import json
import logging
from collections import namedtuple
from datetime import datetime
from functools import lru_cache
from typing import Iterable, Any, Mapping, Tuple, List

import numpy as np
import pandas as pd

from kisters.water.time_series.core.time_series_decorator import TimeSeriesDecorator
from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.core.time_series_store import TimeSeriesStore

CommitData = namedtuple('CommitData', ['df', 'start', 'end', 'quality'])
CommitComments = namedtuple('CommitComments', ['df', 'category'])
LOG = logging.getLogger(__name__)


class _CacheTimeSeries(TimeSeriesDecorator):
    def __init__(self, forward: TimeSeries):
        super().__init__(forward)
        self._data = None
        self._comments = None
        self._commit_cache_data: List[CommitData] = []
        self._commit_cache_comments: List[CommitComments] = []

    def _load_data_frame(self, start: datetime = None, end: datetime = None, params: Mapping = None) -> pd.DataFrame:
        if self._data is None or self._data.shape[0] == 0:
            self._data = self._forward.read_data_frame(start, end, params=params)
            return self._data.copy()

        if start is None:
            start = self.coverage_from
        if end is None:
            end = self.coverage_until

        dates = self._data.index
        if start < dates[0]:
            df = self._forward.read_data_frame(start, dates[0], params=params)
            self._data = pd.concat([df[~df.index.isin(self._data.index)], self._data])
        if end > dates[-1]:
            df = self._forward.read_data_frame(dates[-1], end, params=params)
            self._data = pd.concat([self._data, df[~df.index.isin(self._data.index)]])

        if start is None and end is None:
            return self._data.copy()
        if start is None:
            return self._data.loc[self._data.index <= end].copy()
        elif end is None:
            return self._data.loc[self._data.index >= start].copy()
        else:
            return self._data.loc[(self._data.index >= start) & (self._data.index <= end)].copy()

    def __remove_gaps(self, data_frame: pd.DataFrame, start: datetime, end: datetime):
        if start is not None and start < data_frame.index[0]:
            if start <= self._data.index[0]:
                self._data.drop(self._data.index[self._data.index < data_frame.index[0]])
            else:
                self._data.loc[(start <= self._data.index) & (self._data.index < data_frame.index[0]), :] = np.nan
        if end is not None and end > data_frame.index[-1]:
            if end >= self._data.index[-1]:
                self._data.drop(self._data.index[self._data.index > data_frame.index[-1]])
            else:
                self._data.loc[(data_frame.index[-1] < self._data.index) & (self._data.index <= end), :] = np.nan

    @classmethod
    def __aggregate_commit_data(cls, commit_data, df_aux, aux_start, aux_end):
        remove_index = False
        if df_aux.index[0] <= commit_data.df.index[0] and df_aux.index[-1] >= commit_data.df.index[-1]:
            remove_index = True
        elif aux_start == df_aux.index[0] and aux_end == df_aux.index[-1]:
            if aux_start <= commit_data.df.index[-1] and aux_end >= commit_data.df.index[0]:
                remove_index = True
            df_aux = pd.concat([df_aux, commit_data.df[~commit_data.df.index.isin(df_aux.index)]], sort=True)
        elif ((aux_start == df_aux.index[0] and aux_start <= commit_data.df.index[-1] <= df_aux.index[-1])
              or (aux_end == df_aux.index[-1] and df_aux.index[0] <= commit_data.df.index[0] <= aux_end)):
            remove_index = True
            df_aux = pd.concat([df_aux, commit_data.df[~commit_data.df.index.isin(df_aux.index)]], sort=True)
        return remove_index, df_aux

    def __update_commit_data(self, data_frame: pd.DataFrame, start: datetime, end: datetime):
        aux_start = start if start is not None else data_frame.index[0]
        aux_end = end if end is not None else data_frame.index[-1]
        df_aux = data_frame
        indices_to_remove = []
        for i, commit_data in enumerate([c for c in self._commit_cache_data if not c.quality]):
            remove_index, df_aux = self.__aggregate_commit_data(commit_data, df_aux, aux_start, aux_end)
            if remove_index:
                indices_to_remove.append(i)
                aux_start = aux_start if aux_start <= commit_data.start else commit_data.start
                aux_end = aux_end if aux_end >= commit_data.end else commit_data.end

        for i in indices_to_remove:
            del self._commit_cache_data[i]
        self._commit_cache_data.append(CommitData(df_aux, aux_start, aux_end, False))

    def write_data_frame(self, data_frame: pd.DataFrame, start: datetime=None, end: datetime=None):
        mask = None
        if start is not None:
            mask = data_frame.index >= start
        if end is not None:
            mask = data_frame.index <= end if mask is None else mask & (data_frame.index <= end)
        if mask is not None:
            data_frame = data_frame.loc[mask]

        self._load_data_frame(data_frame.index[0], data_frame.index[-1])
        self._data = pd.concat([self._data, data_frame[~data_frame.index.isin(self._data.index)]], sort=True)
        self._data.update(data_frame)
        self._data = self._data.reindex(self._data.index.sort_values())
        if start is not None or end is not None:
            self.__remove_gaps(data_frame, start, end)
        self.__update_commit_data(data_frame, start, end)

    def __first_comment(self) -> datetime:
        date = None
        for i, row in self._comments.iterrows():
            if date is None:
                date = row.loc['from']
            date = row.loc['from'] if row.loc['from'] < date else date
        return date

    def __last_comment(self) -> datetime:
        date = None
        for i, row in self._comments.iterrows():
            if date is None:
                date = row.loc['until']
            date = row.loc['until'] if row.loc['until'] > date else date
        return date

    def __initialize_comments(self, start: datetime, end: datetime):
        if hasattr(self._forward, 'get_comments'):
            self._comments = self._forward.get_comments(start, end)
            self._comments['from'] = pd.to_datetime(self._comments['from'], utc=True)
            self._comments['until'] = pd.to_datetime(self._comments['until'], utc=True)
        else:
            self._comments = pd.DataFrame(columns=['from', 'until', 'comment'])

    def __retrieve_and_update_comments(self, start: datetime, end: datetime):
        first_comment = self.__first_comment()
        last_comment = self.__last_comment()
        if start < first_comment and hasattr(self._forward, 'get_comments'):
            self.write_comments(self._forward.get_comments(start, first_comment))
        if end > last_comment and hasattr(self._forward, 'get_comments'):
            self.write_comments(self._forward.get_comments(end, last_comment))

    def __filter_comments(self, start: datetime, end: datetime) -> pd.DataFrame:
        comments = self._comments.copy()
        for i, row in comments.iterrows():
            if end < row.loc['from'] or row.loc['until'] < start:
                comments = comments.drop(i)
            else:
                if row.loc['from'] < start:
                    comments.loc[i, 'from'] = start
                if row.loc['until'] > end:
                    comments.loc[i, 'until'] = end
        return comments

    def get_comments(self, start: datetime=None, end: datetime=None) -> pd.DataFrame:
        start = self._to_zoned_datetime(start)
        end = self._to_zoned_datetime(end)
        if self._comments is None:
            self.__initialize_comments(start, end)
            return self._comments.copy()
        if self._comments.shape[0] == 0:
            return self._comments.copy()

        if start is None:
            start = self.coverage_from
        if end is None:
            end = self.coverage_until
        self.__retrieve_and_update_comments(start, end)
        return self.__filter_comments(start, end)

    def __merge_comments_helper(self, row: pd.Series, i_: int, row_: pd.Series):
        drop = False
        if row.loc['comment'] == row_.loc['comment']:
            if row.loc['from'] >= row_.loc['from'] and row.loc['until'] <= row_.loc['until']:
                drop = True
            else:
                if row.loc['from'] < row_.loc['from'] <= row.loc['until']:
                    self._comments.loc[i_, 'from'] = row['from']
                    drop = True
                if row.loc['until'] > row_.loc['until'] >= row.loc['from']:
                    self._comments.loc[i_, 'until'] = row['until']
                    drop = True
        return drop

    def write_comments(self, comments: pd.DataFrame, category: int=None):
        if self._comments is None or self._comments.shape[0] == 0:
            self._comments = comments
        else:
            drop_list = []
            for i, row in comments.iterrows():
                add_index = False
                for i_, row_ in self._comments.iterrows():
                    if self.__merge_comments_helper(row, i_, row_):
                        add_index = True
                if add_index:
                    drop_list.append(i)
            comments = comments.drop(drop_list)
            self._comments = pd.concat([self._comments, comments], ignore_index=True, sort=False)
        self._commit_cache_comments.append(CommitComments(comments, category))

    def update_qualities(self, qualities: pd.DataFrame):
        self._load_data_frame(qualities.index[0], qualities.index[-1])
        q_col = list(qualities.columns)[0]
        column_list = list(self._data.columns)
        if q_col not in column_list:
            q_col_name = 'quality'
            for col in column_list:
                if 'qualit' in col:
                    q_col_name = col
            qualities = qualities.rename(index=str, columns={q_col: q_col_name})
        self._data.update(qualities)
        self._commit_cache_data.append(CommitData(qualities, None, None, True))

    def read_data_frame_with_comments(self, start: datetime=None, end: datetime=None):
        df = self.read_data_frame(start, end)
        comments = self.get_comments(start, end)
        df['comment'] = pd.Series([''] * df.shape[0], index=df.index)
        for i, row in comments.iterrows():
            df.loc[(row.loc['from'] <= df.index) & (df.index <= row.loc['until']),
                   ['comment']] = df['comment'].map(
                lambda x: row.loc['comment'] if x == '' else x + ', ' + row.loc['comment'])
        return df

    def commit_changes(self):
        for commit in self._commit_cache_data:
            if commit.quality:
                try:
                    self._forward.update_qualities(commit.df)
                except (AttributeError, NotImplementedError):
                    LOG.warning("Commit wasn't totally completed, "
                                "{} doesn't have method update_qualities()".format(self._forward))
            else:
                super().write_data_frame(commit.df, commit.start, commit.end)
        for comments in self._commit_cache_comments:
            if comments.category is not None:
                params = {'comments': comments.df, 'category': comments.category}
            else:
                params = {'comments': comments.df}
            try:
                self._forward.write_comments(**params)
            except (AttributeError, NotImplementedError):
                LOG.warning("Commit wasn't totally completed, "
                            "{} doesn't have method write_comments()".format(self._forward))
        self._commit_cache_data: List[CommitData] = []
        self._commit_cache_comments: List[CommitComments] = []


class CacheStore(TimeSeriesStore):
    """
    CacheStore is a TimeSeriesStore decorator which allows to cache the retrieval of
    TimeSeries inside the original TimeSeriesStore. Also TimeSeries retrieved this way
    cache the data they contain in memory.

    Args:
        forward: The TimeSeriesStore to be decorated.

    Example:
        .. code-block:: python

            from kisters.water.file_io import FileStore, ZRXPFormat
            from kisters.water.store_decorators import CacheStore
            store = CacheStore(FileStore('tests/data', ZRXPFormat()))
            ts = store.get_by_path('validation/threshold/05BJ004.HG.datum.O')
    """
    def __init__(self, forward: TimeSeriesStore):
        self._forward = forward

    def _get_time_series_list(self, ts_filter: str = None, id_list: Iterable[int] = None,
                              params: Mapping[str, Any] = None) -> Iterable[TimeSeries]:
        if ts_filter is None:
            ts_filter = False
        if id_list is None:
            id_list = False
        else:
            id_list = tuple(id_list)
        if params is None:
            params = {}
        json_params = json.dumps(params)
        return [_CacheTimeSeries(ts) for ts in self.__get_cacheable_time_series_list(ts_filter, id_list, json_params)]

    @lru_cache(maxsize=32)
    def __get_cacheable_time_series_list(self, ts_filter: str, id_list: Tuple[int],
                                         json_params: str) -> Iterable[TimeSeries]:
        if not ts_filter:
            ts_filter = None
        if not id_list:
            id_list = None
        params = json.loads(json_params)
        return self._forward._get_time_series_list(ts_filter, id_list, params)

    def _get_time_series(self, ts_id: int = None, path: str = None, params: Mapping[str, Any] = None) -> TimeSeries:
        if ts_id is None:
            ts_id = False
        if path is None:
            path = False
        if params is None:
            params = {}
        json_params = json.dumps(params)
        return _CacheTimeSeries(self.__get_cacheable_time_series(ts_id, path, json_params))

    @lru_cache(maxsize=512)
    def __get_cacheable_time_series(self, ts_id: int, path: str, json_params: str) -> TimeSeries:
        params = json.loads(json_params)
        if not ts_id:
            ts_id = None
        if not path:
            path = None
        return self._forward._get_time_series(ts_id, path, params)

    def create_time_series(self, path: str, display_name: str, attributes: Mapping = None,
                           params: Mapping[str, Any] = None) -> TimeSeries:
        return self._forward.create_time_series(path, display_name, attributes, params)
