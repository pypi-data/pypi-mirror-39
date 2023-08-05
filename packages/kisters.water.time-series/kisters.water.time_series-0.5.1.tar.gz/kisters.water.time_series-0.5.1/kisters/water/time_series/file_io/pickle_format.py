# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, KISTERS AG, Germany.
# All rights reserved.
# Modification, redistribution and use in source and binary
# forms, with or without modification, are not permitted
# without prior written approval by the copyright holder.
#
# Created on Sat Sep  2 12:13:16 2017
# @author: rs

from datetime import datetime
from typing import Any, Iterable, Mapping, Union

import pandas as pd

from kisters.water.time_series.file_io.time_series_format import TimeSeriesFormat, TimeSeriesReader, TimeSeriesWriter
from kisters.water.time_series.core.time_series import TimeSeries


class PickleFormat(TimeSeriesFormat):
    """
    Pickle formatter class

    Example:
        .. code-block:: python
        
            from kisters.water.file_io import FileStore, PickleFormat
            fs = FileStore('tests/data', PickleFormat())
    """
    def __init__(self):
        super().__init__()
        self._reader = None
        self._writer = None

    @property
    def extensions(self) -> Iterable[str]:
        return ["pkl"]

    @property
    def reader(self) -> TimeSeriesReader:
        if self._reader is None:
            self._reader = PickleReader(self)
        return self._reader

    @property
    def writer(self) -> TimeSeriesWriter:
        if self._writer is None:
            self._writer = PickleWriter(self)
        return self._writer


class PickleReader(TimeSeriesReader):
    def __init__(self, fmt: TimeSeriesFormat=PickleFormat()):
        super().__init__(fmt)

    def _extract_metadata(self, file) -> Iterable[Mapping[str, Any]]:
        ts_meta = self._meta_from_file(file)
        self.format.writer.write_metadata(file, [ts_meta])
        return [ts_meta]

    def load_data_frame(self, file, columns):
        return pd.read_pickle(file)


class PickleWriter(TimeSeriesWriter):
    def __init__(self, fmt: TimeSeriesFormat=PickleFormat()):
        super().__init__(fmt)

    def write(self, file: str, data_list: Union[Iterable[pd.DataFrame], Iterable[TimeSeries]],
              start: datetime=None, end: datetime=None, meta_list: Iterable[Mapping[str, Any]]=None):
        data = list(data_list)[0]
        if isinstance(data, TimeSeries):
            data.read_data_frame(start, end).to_pickle(file)
        else:
            data.to_pickle(file)
