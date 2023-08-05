# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, KISTERS AG, Germany.
# All rights reserved.
# Modification, redistribution and use in source and binary
# forms, with or without modification, are not permitted
# without prior written approval by the copyright holder.
#
# Created on Tue Aug 29 16:29:26 2017
# @author: rs

from datetime import datetime
import logging
from typing import Any, Mapping, TYPE_CHECKING, Union

import pandas as pd
import pytz
from pytz import UnknownTimeZoneError

from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.core.time_series_attributes_mixin import TimeSeriesAttributesMixin
from kisters.water.time_series.core.time_series_cut_range_mixin import TimeSeriesCutRangeMixin
from kisters.water.time_series.core.time_series_item_mixin import TimeSeriesItemMixin
if TYPE_CHECKING:
    from kisters.water.time_series.file_io.time_series_format import TimeSeriesFormat

logger = logging.getLogger(__name__)


class FileTimeSeries(TimeSeriesItemMixin, TimeSeriesAttributesMixin, TimeSeriesCutRangeMixin, TimeSeries):
    def __init__(self, fmt: 'TimeSeriesFormat', meta: Mapping[str, Any]=None):
        super().__init__()
        self.__meta = meta
        self.__fmt = fmt
        self.__meta.setdefault('dataCoverageFrom', None)
        self.__meta.setdefault('dataCoverageUntil', None)
        timezone = self.__format_metadata().get('timezone', 'UTC')
        if 'UTC+' in timezone:
            timezone = 'Etc/GMT-' + timezone.split('+')[-1]
        elif 'UTC-' in timezone:
            timezone = 'Etc/Gmt+' + timezone.split('-')[-1]
        try:
            self._tz = pytz.timezone(timezone)
        except UnknownTimeZoneError:
            self._tz = pytz.timezone('UTC')

    def __init_coverage(self):
        df = self._load_data_frame()
        self.__meta['dataCoverageFrom'] = df.index[0]
        self.__meta['dataCoverageUntil'] = df.index[-1]
        self.__fmt.writer.update_metadata(self.path,
                                          self.metadata[list(self.__fmt.extensions)[0].upper()]['file'],
                                          self.metadata)

    @property
    def coverage_from(self) -> Union[datetime, None]:
        if self.__meta['dataCoverageFrom'] is None:
            self.__init_coverage()
        return pd.to_datetime(self.__meta['dataCoverageFrom'], utc=True)

    @property
    def coverage_until(self) -> Union[datetime, None]:
        if self.__meta['dataCoverageUntil'] is None:
            self.__init_coverage()
        return pd.to_datetime(self.__meta['dataCoverageUntil'], utc=True)

    def _raw_metadata(self) -> Mapping[str, str]:
        return self.__meta

    def __format_metadata(self) -> Mapping[str, Any]:
        return self.__meta[list(self.__fmt.extensions)[0].upper()]

    def _load_data_frame(self, start: datetime=None, end: datetime=None,
                         params: Mapping[str, str]=None) -> pd.DataFrame:
        df = self.__fmt.reader.load_data_frame(
            columns=self.__meta.get('columns'), **self.__format_metadata())

        if start is None and end is None:
            return df
        if start is None:
            mask = df.index <= end
        elif end is None:
            mask = df.index >= start
        else:
            mask = (df.index >= start) & (df.index <= end)
        return df.loc[mask]

    @classmethod
    def write_comments(cls, comments):
        logger.warning("write_comments not implemented. Ignoring {} comments".format(len(comments)))

    @classmethod
    def update_qualities(cls, qualities):
        logger.warning("update_qualities not implemented. Ignoring {} qualities".format(len(qualities)))

    def write_data_frame(self, data_frame: pd.DataFrame, start: datetime=None, end: datetime=None):
        data_inside = self.read_data_frame()
        data = pd.concat([data_inside, data_frame[~data_frame.index.isin(data_inside.index)]], sort=True)
        data.update(data_frame)
        data = data.reindex(data.index.sort_values())
        data = data.drop(data.index[((start <= data.index) & (data.index < data_frame.index[0]))
                         | ((data_frame.index[-1] < data.index) & (data.index <= end))])

        format_meta = self.__format_metadata()
        self.__fmt.writer.write(format_meta['file'], [data], start, end, [self.metadata])
