# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, KISTERS AG, Germany.
# All rights reserved.
# Modification, redistribution and use in source and binary
# forms, with or without modification, are not permitted
# without prior written approval by the copyright holder.
#
# Created on Mon 11  15:04:35 2017
# @author: mrd

import datetime
from typing import Mapping, Any, MutableMapping, TYPE_CHECKING

import dateutil

import pandas as pd
from pandas import DataFrame

from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.core.time_series_attributes_mixin import TimeSeriesAttributesMixin
from kisters.water.time_series.core.time_series_cut_range_mixin import TimeSeriesCutRangeMixin
from kisters.water.time_series.core.time_series_item_mixin import TimeSeriesItemMixin
if TYPE_CHECKING:
    from kisters.water.time_series.tso.tso import TSOStore


class TSOTimeSeries(TimeSeriesItemMixin, TimeSeriesAttributesMixin, TimeSeriesCutRangeMixin, TimeSeries):
    """
    Class for TimeSeries.Online (TSOStore) TimeSeries objects
    """

    def __init__(self, tso: 'TSOStore', ts_json: MutableMapping[str, Any]):
        super(TSOTimeSeries, self).__init__()
        self.__TSO = tso
        self.__data = ts_json

    @property
    def coverage_from(self) -> datetime:
        try:
            c_f = datetime.datetime.fromtimestamp(self.__data['dataFrom'] / 1e3)
        except (OverflowError, OSError, TypeError):
            c_f = dateutil.parser.parse(self.__data['dataFrom'])
        return c_f

    @property
    def coverage_until(self) -> datetime:
        try:
            c_u = datetime.datetime.fromtimestamp(self.__data['dataTo'] / 1e3)
        except (OverflowError, OSError, TypeError):
            c_u = dateutil.parser.parse(self.__data['dataTo'])
        return c_u

    @property
    def short_name(self) -> str:
        short_name = self.path.split("/")[-1:][0]
        return short_name

    @property
    def name(self) -> str:
        return self.__data['name']

    @property
    def id(self) -> str:
        return self.__data['id']

    @property
    def path(self) -> str:
        return self.__data['tsPath']

    @property
    def location(self) -> str:
        return self.__data['locationId']

    def _load_data_frame(self, start: datetime=None, end: datetime=None, params: Mapping[str, Any]=None) -> DataFrame:
        r = self.__TSO._session.get(
            self.__TSO._baseURL + 'organizations/' + self.__data['organization'] +
            '/timeSeries/' + self.id + '/data/?from=' + str(start) + '&to=' + str(end))
        j = r.json()
        raw_data = pd.DataFrame(j.get('data', self.__data.get('data', None)),
                                columns=j.get('columns', self.__data.get('columns', 'timestamp,value')).split(','))
        raw_data['timestamp'] = pd.to_datetime(raw_data['timestamp'], utc=True)
        raw_data = raw_data.set_index('timestamp')
        return raw_data

    def _raw_metadata(self) -> Mapping[str, Any]:
        raw_metadata = self.__data
        r = self.__TSO._session.get(
            self.__TSO._baseURL + 'organizations/' + self.__data['organization'] +
            '/locations/' + self.__data['locationId'])
        raw_metadata.update({'location': r.json()})
        return raw_metadata

    def write_data_frame(self, data_frame: DataFrame, start: datetime=None, end: datetime=None):
        raise NotImplementedError
