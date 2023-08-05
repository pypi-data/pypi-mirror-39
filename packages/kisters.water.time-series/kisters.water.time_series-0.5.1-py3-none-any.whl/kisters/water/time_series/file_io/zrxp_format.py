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

import datetime
import os
import re
from tempfile import mkstemp
from typing import Iterable, List, Mapping, TextIO, Any, Optional, Tuple, Union

import numpy as np
import pandas as pd
from pytz import UnknownTimeZoneError

from kisters.water.time_series.file_io.time_series_format import TimeSeriesFormat, TimeSeriesReader, TimeSeriesWriter
from kisters.water.time_series.core.time_series import TimeSeries


READ_SIZE = 10 * 1024 * 1024
ZRXP_ENCODING = 'iso-8859-1'
HEADER_KEYS = {
    "SNAME": "stationName",
    "SANR": "stationNumber",
    "SWATER": "water",
    "CDASA": "dataLogger",
    "CDASANAME": "dataLoggerName",
    "CCHANNEL": "channelName",
    "CCHANNELNO": "channel",
    "CMW": "valuesPerDay",
    "CNAME": "parameterName",
    "CNR": "parameterNumber",
    "CUNIT": "unit",
    "REXCHANGE": "exchangeNumber",
    "RINVAL": "invalidValue",
    "RTIMELVL": "timeLevel",
    "XVLID": "id",
    "TSPATH": "tsPath",
    "CTAG": None,
    "CTAGKEY": None,
    "XTRUNCATE": None,
    "METCODE": None,
    "METERNUMBER": None,
    "EDIS": None,
    "TZ": "timezone",
    "ZDATE": None,
    "ZRXPVERSION": None,
    "ZRXPCREATOR": None,
    "LAYOUT": None,
    "TASKID": None,
    "SOURCESYSTEM": "sourceSystem",
    "SOURCEID": "sourceId"
}


class ZRXPLayoutError(Exception):
    def __init__(self, layout_diff):
        self.layout_diff = layout_diff

    def __str__(self):
        return repr(self.layout_diff)


class ZRXPFormat(TimeSeriesFormat):
    """
    ZRXP formatter class

    Example:
        .. code-block:: python

            from kisters.water.file_io import FileStore, ZRXPFormat
            fs = FileStore('tests/data', ZRXPFormat())
    """
    def __init__(self):
        super().__init__()
        self._reader = None
        self._writer = None

    @property
    def extensions(self) -> Iterable[str]:
        return ["zrx", "zrxp"]

    @property
    def reader(self) -> TimeSeriesReader:
        if self._reader is None:
            self._reader = ZRXPReader(self)
        return self._reader

    @property
    def writer(self) -> TimeSeriesWriter:
        if self._writer is None:
            self._writer = ZRXPWriter(self)
        return self._writer


class ZRXPReader(TimeSeriesReader):
    def __init__(self, fmt: TimeSeriesFormat=ZRXPFormat(), default_quality: int=200, default_interpolation: int=2):
        super().__init__(fmt)
        self._default_quality = default_quality
        self._default_interpolation = default_interpolation

    def _read_metadata(self, file: str, lines: Iterable[str]):
        ts_meta = self._meta_from_file(file)
        for line in lines:
            for part in line[1:].strip().replace(';*;', '|*|').split('|*|'):
                part = part.strip()
                for key, value in HEADER_KEYS.items():
                    if part.startswith(key):
                        ts_meta[key] = part[len(key):]
                        if value is not None:
                            ts_meta[value] = ts_meta[key]
        ts_meta['columns'] = self.__extract_columns(ts_meta.get('LAYOUT', None))
        return ts_meta

    @classmethod
    def __process_metadata_offsets(cls, newlines: np.ndarray, metas: np.ndarray,
                                   data_offsets: np.ndarray, header_offsets: np.ndarray,
                                   i: int, read_count: int):
        found = False
        move = 1
        ix = np.where(newlines == metas[i])[0]
        for j in range(i + 1, metas.shape[0]):
            move += 1
            if ix + j - i >= newlines.shape[0]:
                break
            if metas[j] != newlines[ix + j - i]:
                found = True
                data_offsets = np.append(data_offsets, newlines[ix + j - i])
                if data_offsets.shape[0] > header_offsets.shape[0]:
                    header_offsets = np.append(header_offsets, metas[i])
                break
        if not found:
            if ix + metas.shape[0] < newlines.shape[0]:
                data_offsets = np.append(data_offsets, newlines[ix + metas.shape[0]])
            if read_count != 0 and data_offsets.shape[0] >= header_offsets.shape[0]:
                header_offsets = np.append(header_offsets, metas[i])
        return header_offsets, data_offsets, move

    @classmethod
    def __process_offsets(cls, metas, newlines, read_count):
        header_offsets = np.empty([0], dtype=np.longlong)
        data_offsets = np.empty([0], dtype=np.longlong)
        if read_count == 0:
            metas = metas[1:]
            header_offsets = np.append(header_offsets, 0)
        i = 0
        while i < metas.shape[0]:
            header_offsets, data_offsets, move = cls.__process_metadata_offsets(newlines, metas, data_offsets,
                                                                                header_offsets, i, read_count)
            i += move
        if metas.shape[0] == 0 and header_offsets.shape[0] > data_offsets.shape[0]:
            data_offsets = np.append(data_offsets, newlines[0])
        return header_offsets, data_offsets

    @classmethod
    def __process_n_rows(cls, header_offsets, data_offsets, newlines, read_count):
        meta_n_rows = np.empty([0], dtype=np.longlong)
        if header_offsets.shape[0] > 0 and read_count > 0:
            meta_n_rows = np.append(meta_n_rows, np.where(newlines < header_offsets[0])[0].shape[0])
        for i in range(data_offsets.shape[0]):
            if i + 1 < header_offsets.shape[0]:
                meta_n_rows = np.append(meta_n_rows, np.where((data_offsets[i] <= newlines) &
                                                            (newlines < header_offsets[i + 1]))[0].shape[0])
            else:
                meta_n_rows = np.append(meta_n_rows, np.where(data_offsets[i] <= newlines)[0].shape[0])
        if meta_n_rows.shape[0] == 0:
            meta_n_rows = np.append(meta_n_rows, newlines.shape[0])
        return meta_n_rows

    def __process_metadata_bytes(self, ts_metas: List, incomplete_meta: Optional[str],
                                 file: str, data_offsets: np.ndarray, header_offsets: np.ndarray,
                                 aux: np.ndarray) -> Tuple[List[Any], Optional[bytes]]:
        if incomplete_meta is not None and data_offsets.shape[0] > 0:
            metadata = incomplete_meta + aux[:data_offsets[0]].tostring().decode(ZRXP_ENCODING)
            ts_metas.append(self._read_metadata(file, metadata.splitlines()))
            incomplete_meta = None
        for i in range(header_offsets.shape[0]):
            if i < data_offsets.shape[0]:
                ts_metas.append(self._read_metadata(
                    file, aux[header_offsets[i]:data_offsets[i]].tostring().decode(ZRXP_ENCODING).splitlines()))
            else:
                incomplete_meta = aux[header_offsets[i]:].tostring().decode(ZRXP_ENCODING)
        return ts_metas, incomplete_meta

    def _extract_metadata(self, file: str) -> List:
        read_count = 0
        do_count = 0
        mn_count = 0
        ext_key = list(self._format.extensions)[0].upper()
        f = open(file, 'rb')
        ts_metas = []
        incomplete_meta = None
        while True:
            buff = f.read(READ_SIZE)
            if buff == b'':
                break
            aux = np.frombuffer(buff, dtype=np.uint8, count=len(buff))
            metas = np.where(aux == 35)[0]
            newlines = np.where(aux == 10)[0] + 1
            header_offsets, data_offsets = self.__process_offsets(metas, newlines, read_count)
            meta_nrows = self.__process_n_rows(header_offsets, data_offsets, newlines, read_count)

            ts_metas, incomplete_meta = self.__process_metadata_bytes(ts_metas, incomplete_meta, file,
                                                                      data_offsets, header_offsets, aux)

            # AGGREGATE TOTALS
            for i in range(len(data_offsets)):
                ts_metas[do_count][ext_key]['data_offset'] = data_offsets[i] + read_count * READ_SIZE
                ts_metas[do_count][ext_key]['invalid'] = float(ts_metas[do_count].get('RINVAL', -777.0))
                ts_metas[do_count][ext_key]['timezone'] = ts_metas[do_count].get('TZ', 'UTC')
                do_count += 1
            for i in range(len(meta_nrows)):
                if i == 0 and mn_count > 0:
                    ts_metas[mn_count - 1][ext_key]['nrows'] += meta_nrows[i]
                else:
                    ts_metas[mn_count][ext_key]['nrows'] = meta_nrows[i]
                    mn_count += 1
            read_count += 1
        f.close()
        self.format.writer.write_metadata(file, ts_metas)
        return ts_metas

    @classmethod
    def __check_layout_consistency(cls, df_columns: List[str], columns: List[str]) -> List[str]:
        diff = len(df_columns) - len(columns)
        if diff < 0 or diff > 2:
            raise ZRXPLayoutError(diff)
        else:
            if diff == 1:
                if 'value.quality' in columns:
                    columns.append('value.interpolation')
                else:
                    columns.append('value.quality')
            elif diff == 2:
                columns.append('value.quality')
                columns.append('value.interpolation')
        return columns

    @classmethod
    def __localize_timestamps(cls, df_index: pd.DatetimeIndex, timezone: str) -> pd.DatetimeIndex:
        if 'UTC+' in timezone:
            timezone = 'Etc/GMT-' + timezone.split('+')[-1]
        elif 'UTC-' in timezone:
            timezone = 'Etc/Gmt+' + timezone.split('-')[-1]
        try:
            return df_index.tz_localize(timezone)
        except UnknownTimeZoneError:
            return df_index.tz_localize('UTC')

    def load_data_frame(self, file: str, data_offset: int, columns: List[str], nrows: int=None,
                        invalid: float=-777.0, timezone: str='UTC') -> pd.DataFrame:
        if 'status' in columns:
            columns[columns.index('status')] = 'value.quality'
        if 'interpolation_type' in columns:
            columns[columns.index('interpolation_type')] = 'value.interpolation'
        with open(file, 'rb') as f:
            f.seek(int(data_offset))
            df = pd.read_csv(f, engine='c', header=None, nrows=int(nrows), sep=r'\s+')
            df.columns = self.__check_layout_consistency(df.columns, columns)
            df.columns = columns
            df = df.set_index('timestamp')
            df.index = pd.to_datetime(df.index, format='%Y%m%d%H%M%S')
            df.index = self.__localize_timestamps(df.index, timezone)
            df.loc[df['value'] == invalid, ['value']] = np.nan
            if 'value.quality' in columns:
                quality_col = 'value.quality'
                df.loc[df[quality_col] < 0, ['value']] = np.nan
            return df

    @classmethod
    def __extract_columns(cls, config: str) -> List[str]:
        if config is None:
            return ['timestamp', 'value']
        columns = []
        found = re.search('\\(([^)]+)\\)', config)

        if not found or not found.group(1):
            raise Exception("Invalid layout '{}'".format(config))
        for i in found.group(1).split(","):
            columns.append(i.strip())
        if 'timestamp' not in columns:
            raise Exception("Missing timestamp in layout '{}'".format(config))
        if 'value' not in columns:
            raise Exception("Missing value in layout '{}'".format(config))
        return columns

    def _extract_data_line(self, line: str, inv: float, pos_date: int, pos_value: int, pos_status: int) -> List:
        blocks = line.split()
        time = datetime.datetime.strptime(blocks[pos_date], '%Y%m%d%H%M%S')
        data = np.double(blocks[pos_value])
        quality = self._default_quality
        if pos_status is not None and len(blocks) > pos_status:
            quality = np.int(blocks[pos_status])
        if data == inv or quality < 0:
            data = None
        return [time, [data, self._default_interpolation, quality]]


class ZRXPWriter(TimeSeriesWriter):
    def __init__(self, fmt: ZRXPFormat=ZRXPFormat()):
        super().__init__(fmt)

    def write(self, file: str, data_list: Union[Iterable[pd.DataFrame], Iterable[TimeSeries]],
              start: datetime=None, end: datetime=None,
              meta_list: Iterable[Mapping[str, Any]]=None):
        fd, path = mkstemp()
        with open(path, 'w') as fh:
            for i, ts in enumerate(data_list):
                if isinstance(ts, TimeSeries):
                    self._write_block(fh, ts, start, end)
                else:
                    self._write_block(fh, ts, start, end, meta_list[i])
        if os.path.isfile(file):
            os.unlink(file)
        os.close(fd)
        os.rename(path, file)
        if os.path.isfile(file + '.metadata'):
            os.unlink(file + '.metadata')

    def _write_block(self, fh: TextIO, ts: Union[pd.DataFrame, TimeSeries], start: datetime, end: datetime,
                     metadata: Mapping[str, Any]=None):
        if isinstance(ts, TimeSeries):
            data = ts.read_data_frame(start, end)
            metadata = ts.metadata
        else:
            data = ts
        self._write_header(fh, metadata, data)
        self._write_data(fh, data)

    def _write_header(self, fh: TextIO, metadata: Mapping[str, Any], data: pd.DataFrame):
        fh.write("#" + "|*|".join(self._header_values(metadata)) + "\n")
        layout = "#LAYOUT(timestamp,value"
        if 'value.status' in data.columns.values or 'value.quality' in data.columns.values:
            layout += ',status'
        if 'value.interpolation' in data.columns.values:
            layout += ',interpolation_type'
        layout += ")|*|\n"
        fh.write(layout)

    @classmethod
    def _header_values(cls, metadata: Mapping[str, Any]):
        values = ["RINVAL-777"]
        for k, v in HEADER_KEYS.items():
            if v in metadata:
                values.append(k + str(metadata[v]))
        return values

    @classmethod
    def _write_data(cls, fh: TextIO, data: pd.DataFrame):
        def nop(fh, row):
            pass
        write_quality = nop
        write_value = nop
        write_interpolation = nop

        columns = data.columns.values
        for i in range(len(columns) - 1, -1, -1):
            if 'value' == columns[i]:
                cv = columns[i]

                def value(fh, row):
                    fh.write(" ")
                    v = row[cv]
                    if v is None:
                        v = -777
                    fh.write(str(v))
                write_value = value

            if 'quality' in columns[i] or 'status' in columns[i]:
                cq = columns[i]

                def quality(fh, row):
                    fh.write(" ")
                    fh.write(str(int(row[cq])))
                write_quality = quality

            if 'interpolation' in columns[i]:
                ci = columns[i]

                def interpolation(fh, row):
                    fh.write(" ")
                    fh.write(str(int(row[ci])))
                write_interpolation = interpolation

        for index, row in data.iterrows():
            fh.write(index.strftime("%Y%m%d%H%M%S"))
            write_value(fh, row)
            write_quality(fh, row)
            write_interpolation(fh, row)
            fh.write("\n")
        fh.write("\n")
