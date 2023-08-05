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

import csv
from csv import DictWriter
from datetime import datetime
from typing import Any, Callable, Iterable, Mapping, TextIO, List, Union

import pandas as pd

from kisters.water.time_series.file_io.time_series_format import TimeSeriesFormat, TimeSeriesReader, TimeSeriesWriter
from kisters.water.time_series.core.time_series import TimeSeries


def writer(file: TextIO, delimiter: str, quotechar: str) -> DictWriter:
    w = csv.writer(file, delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    return w


class CSVFormat(TimeSeriesFormat):
    """
    CSV formatter class

    Example:
        .. code-block:: python

            from kisters.water.file_io import FileStore, CSVFormat
            fs = FileStore('tests/data', CSVFormat())
    """
    def __init__(self, delimiter: str=',', quotechar: str='"', header_lines: int=1):
        super().__init__()
        self._delimiter = delimiter
        self._quotechar = quotechar
        self._header_lines = header_lines
        self._writer = None
        self._reader = None

    @property
    def extensions(self) -> Iterable[str]:
        return ["csv"]

    @property
    def reader(self) -> TimeSeriesReader:
        if self._reader is None:
            self._reader = CSVReader(self, self._header_lines, self._delimiter, self._quotechar)
        return self._reader

    @property
    def writer(self) -> TimeSeriesWriter:
        if self._writer is None:
            self._writer = CSVWriter(self, writer, self._delimiter, self._quotechar)
        return self._writer


class CSVReader(TimeSeriesReader):
    def __init__(self, fmt: CSVFormat=CSVFormat(), header_lines: int=1, delimiter: str=',', quotechar: str='"'):
        super().__init__(fmt)
        self._header_lines = header_lines
        self._delimiter = delimiter
        self._quotechar = quotechar

    def _extract_metadata(self, file) -> Iterable[Mapping[str, Any]]:
        ts_meta = self._meta_from_file(file)
        with open(file, 'r') as f:
            for i in range(self._header_lines):
                ts_meta.update(self.__process_metadata_line(f.readline()))
        self.format.writer.write_metadata(file, [ts_meta])
        return [ts_meta]

    def load_data_frame(self, file: str, columns: List[str]):
        df = pd.read_csv(file, engine='c', skiprows=self._header_lines - 1,  # skiprows is 0-indexed
                         sep=self._delimiter, quotechar=self._quotechar)
        df.columns = columns
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        df = df.set_index('timestamp')
        return df

    @classmethod
    def __process_metadata_line(cls, line: str) -> Mapping[str, Any]:
        return {'columns': line.split(',')}


class CSVWriter(TimeSeriesWriter):
    def __init__(self, fmt: CSVFormat=CSVFormat(), writer: Callable=writer, delimiter: str=None, quotechar: str=None):
        super().__init__(fmt)
        self._writer = writer
        self._delimiter = delimiter
        self._quotechar = quotechar

    def write(self, file: str, data_list: Union[Iterable[pd.DataFrame], Iterable[TimeSeries]],
              start: datetime=None, end: datetime=None, meta_list: Iterable[Mapping[str, Any]]=None):
        with open(file, 'w') as fh:
            for ts in data_list:
                if isinstance(ts, TimeSeries):
                    ts = ts.read_data_frame(start, end)
                self._write_block(fh, ts)

    def _write_block(self, fh: TextIO, df: pd.DataFrame):
        writer = self._writer(fh, delimiter=self._delimiter, quotechar=self._quotechar)
        self._write_header(writer, ['timestamp'] + df.columns.tolist())
        df.reset_index().to_csv(fh, sep=self._delimiter, quotechar=self._quotechar,
                                index=False, header=False)

    @classmethod
    def _write_header(cls, writer: DictWriter, columns: List[str]):
        writer.writerow(columns)
