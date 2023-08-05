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

import re
import requests
from typing import Mapping, Any, Iterable

from requests import HTTPError

from kisters.water.time_series.core.time_series import TimeSeries
from kisters.water.time_series.core.time_series_store import TimeSeriesStore
from kisters.water.time_series.tso.tso_time_series import TSOTimeSeries


class TSOStore(TimeSeriesStore):
    """
    Class to provide a simple backend for TimeSeries.Online to retrieve time series data via REST interfaces.
    """

    def __init__(self, user: str, password: str, organisation: str, base_url: str):
        """
        Initialize login data and establish connection via TSO REST interface.

        Args:
            user: username for TimeSeriesOnline.
            password: password for the TimeSeriesOnline user.
            organisation: TimeSeriesOnline organisation to access.
            base_url: TimeSeriesOnline base url.
        """
        super(TSOStore, self).__init__()
        self._user = user
        self._password = password
        self._organisation = organisation
        self._baseURL = base_url
        self.__connect__(user, password)

    def __connect__(self, user: str, password: str):
        login_credentials = {'userName': user, 'password': password}
        self._session = requests.Session()
        self._session.post(self._baseURL + 'auth/login/', json=login_credentials)

    def _get_time_series(self, ts_id: str=None, path: str=None, params: Mapping[str, Any]=None) -> TimeSeries:
        """
            Method to return a TSO time series object.
        Args:
            ts_id: the ts id (e.g. "8a021695-96bb-484f-ba00-818edf2c1967").
            path: the ts path (e.g. "68/190/Bue/Cmd.P").
            params: the additional parameters which are passed to the REST API.

        Returns:
            The selected TimeSeries object with the id given.
        """
        try:
            ts = []
            if ts_id is not None:
                ts = self._get_time_series_list(id_list=[ts_id])
            elif path is not None:
                ts = self._get_time_series_list(ts_filter=path)
            ts = ts[0]
        except (HTTPError, IndexError):
            raise KeyError('Requested TimeSeries does not exist.')
        return ts

    @classmethod
    def __filter_by_pattern(cls, ts_list_json: Iterable[Mapping[str, Any]], ts_filter: str):
        filtered_list = []
        if ts_filter is not None:
            exp = re.compile(ts_filter.replace(".", "\\.").replace(
                "/", "\\/").replace("?", "\\?").replace("*", ".*"))
            for ts in ts_list_json:
                path = ts['tsPath']
                if path == ts_filter or exp.match(str(path)):
                    filtered_list.append(ts)
            return filtered_list
        else:
            return ts_list_json

    @classmethod
    def __filter_by_id_list(cls, ts_list_json: Iterable[Mapping[str, Any]], id_list: Iterable[str]=None):
        filtered_list = []
        if ts_list_json is not None and id_list is not None:
            for item in ts_list_json:
                if item["id"] in id_list:
                    filtered_list.append(item)
            return filtered_list
        else:
            return ts_list_json

    def _get_time_series_list(self, ts_filter: str=None, id_list: Iterable[str]=None,
                              params: Mapping[str, Any]=None) -> Iterable[TimeSeries]:
        """
            Get a TSO time series list and return a list of (selected/filtered) TimeSeries objects (as json/dict's).
        Args:
            ts_filter: the filtering key for the time series JSON representation (masking the PATH of a single ts).
            id_list: the filtering keys [list] for the time series JSON representations (multiple ts selection).
            params: the additional parameters which are passed to the rest api.

        Returns:
            The list of TimeSeries objects corresponding to the ts_filter and id_list.
        """

        resource = self._session.get(self._baseURL + "organizations/" + self._organisation + "/timeSeries/",
                                     params=params)
        ts_list = resource.json()
        tso_list = []
        ts_list = self.__filter_by_pattern(ts_list, ts_filter)
        ts_list = self.__filter_by_id_list(ts_list, id_list)
        for dict_item in ts_list:
            tso_list.append(TSOTimeSeries(self, dict_item))
        return tso_list

    def create_time_series(self, path: str, display_name: str, attributes: Mapping[str, Any]=None,
                           params: Mapping[str, Any]=None) -> TimeSeries:
        raise NotImplementedError
