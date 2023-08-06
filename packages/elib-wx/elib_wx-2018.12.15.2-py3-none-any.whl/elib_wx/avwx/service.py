# coding=utf-8
"""
Michael duPont - michael@mdupont.com
Original source: https://github.com/flyinactor91/AVWX-Engine
Modified by etcher@daribouca.net
"""
# pylint: disable=too-many-branches,too-many-boolean-expressions,too-many-return-statements,bad-continuation
# pylint: disable=not-callable,signature-differs
import logging
import typing

import requests
from xmltodict import parse as parsexml

from elib_wx.avwx.core import valid_station
from elib_wx.avwx.exceptions import InvalidRequestError, SourceError

LOGGER = logging.getLogger('elib.wx')


class Service:
    """
    Base Service class for fetching reports
    """

    # Service URL must accept report type and station via .format()
    url: str
    method: str = 'GET'

    def __init__(self, request_type: str) -> None:
        self.rtype = request_type

    def make_err(self, body: str, key: str = 'report path') -> InvalidRequestError:
        """
        Returns an InvalidRequest exception with formatted error message
        """
        msg = f'Could not find {key} in {self.__class__.__name__} response\n'
        return InvalidRequestError(msg + body)

    def _extract(self, raw: str, station: str = None) -> str:
        """
        Extracts report from response. Implemented by child classes
        """
        raise NotImplementedError()

    def fetch(self, station: str) -> str:
        """
        Fetches a report string from the service
        """
        LOGGER.debug('%s: %s: fetching data for station', self.__class__.__name__, station)
        valid_station(station)
        try:
            resp = getattr(requests, self.method.lower())(self.url.format(self.rtype, station))
            if resp.status_code != 200:
                raise SourceError(f'{self.__class__.__name__} server returned {resp.status_code}')
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f'Unable to connect to {self.__class__.__name__} server')
        LOGGER.debug('%s: %s: extracting report', self.__class__.__name__, station)
        report = self._extract(resp.text, station)
        # This split join replaces all *whitespace elements with a single space
        report = ' '.join(report.split())
        LOGGER.debug('%s: %s: report: %s', self.__class__.__name__, station, report)
        return report


class NOAA(Service):
    """
    Requests data from NOAA ADDS
    """

    url = (
        'https://aviationweather.gov/adds/dataserver_current/httpparam'
        '?dataSource={0}s'
        '&requestType=retrieve'
        '&format=XML'
        '&stationString={1}'
        '&hoursBeforeNow=2'
    )

    def _extract(self, raw: str, station: str = None) -> str:
        """
        Extracts the raw_report element from XML response
        """
        LOGGER.debug('%s: %s: extracting report from XML data', self.__class__.__name__, station)
        resp = parsexml(raw)
        LOGGER.debug('%s: %s: extraction successful', self.__class__.__name__, station)
        try:
            report = resp['response']['data'][self.rtype.upper()]
        except KeyError:
            raise self.make_err(raw)
        # Find report string
        if isinstance(report, dict):
            LOGGER.debug('%s: %s: received a single report', self.__class__.__name__, station)
            report = report['raw_text']
        elif isinstance(report, list) and report:
            LOGGER.debug('%s: %s: received %s reports, using first one', self.__class__.__name__, station, len(report))
            report = report[0]['raw_text']
        else:
            raise self.make_err(raw, '"raw_text"')
        # Remove excess leading and trailing data
        LOGGER.debug('%s: %s: stripping extra data', self.__class__.__name__, station)
        for item in (self.rtype.upper(), 'SPECI'):
            if report.startswith(item + ' '):
                report = report[len(item) + 1:]
        LOGGER.debug('%s: %s: returning report: %s', self.__class__.__name__, station, report)
        return report


class AMO(Service):
    """
    Requests data from AMO KMA for Korean stations
    """

    url = 'http://amoapi.kma.go.kr/amoApi/{0}?icao={1}'

    def _extract(self, raw: str, station: str = None) -> str:
        """
        Extracts the report message from XML response
        """
        resp = parsexml(raw)
        try:
            report = resp['response']['body']['items']['item'][self.rtype.lower() + 'Msg']
        except KeyError:
            raise self.make_err(raw)
        # Replace line breaks
        report = report.replace('\n', '')
        # Remove excess leading and trailing data
        for item in (self.rtype.upper(), 'SPECI'):
            if report.startswith(item + ' '):
                report = report[len(item) + 1:]
        report = report.rstrip('=')
        # Make every element single-spaced and stripped
        return ' '.join(report.split())


class MAC(Service):
    """
    Requests data from Meteorologia Aeronautica Civil for Columbian stations
    """

    url = 'http://meteorologia.aerocivil.gov.co/expert_text_query/parse?query={0}%20{1}'
    method = 'POST'

    def _extract(self, raw: str, station: str = None) -> str:
        """
        Extracts the reports message using string finding
        """
        if station is None:
            raise ValueError('station is missing')
        report = raw[raw.find(station.upper() + ' '):]
        report = report[:report.find(' =')]
        return report


PREFERRED = {
    'RK': AMO,
    'SK': MAC,
}


def get_service(station: str) -> typing.Type[Service]:
    """
    Returns the preferred service for a given station
    """
    for prefix in PREFERRED:
        if station.startswith(prefix):
            return PREFERRED[prefix]
    return NOAA
