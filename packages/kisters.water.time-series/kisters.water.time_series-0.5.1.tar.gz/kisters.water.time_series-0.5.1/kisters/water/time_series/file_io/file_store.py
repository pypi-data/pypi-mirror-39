# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, KISTERS AG, Germany.
# All rights reserved.
# Modification, redistribution and use in source and binary
# forms, with or without modification, are not permitted
# without prior written approval by the copyright holder.
#
# Created on Sat Sep  2 12:38:39 2017
# @author: rs

import os
import re
from typing import Any, Iterable, List, Mapping, Union

from pandas.compat import FileNotFoundError

from kisters.water.time_series.file_io.time_series_format import TimeSeriesFormat
from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.core.time_series_store import TimeSeriesStore


class FileStore(TimeSeriesStore):
    """FileStore provides a TimeSeriesStore for your local time series data files

    Args:
        root_dir: The path to your time series data folder.
        file_format: The format used by your time series data files.

    Examples:
        .. code-block:: python

            from kisters.water.file_io import FileStore, ZRXPFormat
            fs = FileStore('tests/data', ZRXPFormat())
            ts = fs.get_by_path('validation/inner_consistency1/station1/H')
    """
    def __init__(self, root_dir: str, file_format: TimeSeriesFormat):
        file_format._TimeSeriesFormat__root_dir = root_dir
        self.__file_format = file_format
        self.__root_dir = root_dir
        if not os.path.isdir(self.__root_dir):
            raise FileNotFoundError(
                "Path " + os.path.abspath(self.__root_dir) + " does not exist")

    def create_time_series(self, path: str, display_name: str, attributes: Mapping[str, Any]=None,
                           params: Mapping[str, Any]=None) -> TimeSeries:
        raise NotImplementedError

    def _get_time_series_list(self, ts_filter: str=None, id_list: List[int]=None,
                              params: Mapping[str, Any]=None) -> Iterable[TimeSeries]:
        ts_list = []
        for f in self._file_list(self.__root_dir):
            ts_list.extend(self.__file_format.reader.read(f))
        ts_list = self._filter(ts_list, ts_filter)
        ts_list = self._filter_id_list(ts_list, id_list)
        return ts_list

    @classmethod
    def _filter(cls, ts_list: Iterable[TimeSeries], ts_filter: str) -> Iterable[TimeSeries]:
        if ts_filter is None:
            return ts_list
        result = []
        exp = re.compile(ts_filter.replace(".", "\\.").replace(
            "/", "\\/").replace("?", "\\?").replace("*", ".*"))
        for ts in ts_list:
            path = ts.path
            if exp.match(path):
                result.append(ts)
        return result

    @classmethod
    def _filter_id_list(cls, ts_list: Iterable[TimeSeries], id_list: Iterable[int]) -> Iterable[TimeSeries]:
        if id_list is None:
            return ts_list
        result = []
        for ts in ts_list:
            ts_id = ts.id
            if (ts_id is not None) and (ts_id in id_list):
                result.append(ts)
        return result

    def _get_time_series(self, ts_id: int=None, path: str=None,
                         params: Mapping[str, Any]=None) -> Union[TimeSeries, None]:
        if params is None:
            params = {"includeDataCoverage": True}
        ts_list = list(self._get_time_series_list(
            ts_filter=path, id_list=[ts_id] if ts_id else None, params=params))
        if len(ts_list) == 0:
            raise KeyError('Requested TimeSeries does not exist.')
        else:
            return ts_list[0]

    def _file_list(self, path: str) -> List[str]:
        file_list = []
        try:
            extensions = self.__file_format.extensions
            for f in os.listdir(path):
                if os.path.isfile(path + "/" + f):
                    for e in extensions:
                        if f.lower().endswith("." + e.lower()):
                            file_list.append(path + '/' + f)
                elif os.path.isdir(path + "/" + f):
                    for ff in self._file_list(path + '/' + f):
                        file_list.append(ff)
        except FileNotFoundError:
            return file_list
        return file_list
