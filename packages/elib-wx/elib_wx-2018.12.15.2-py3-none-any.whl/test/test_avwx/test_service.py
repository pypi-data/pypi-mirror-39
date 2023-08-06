# coding=utf-8
"""
Michael duPont - michael@mdupont.com
Original source: https://github.com/flyinactor91/AVWX-Engine
Modified by etcher@daribouca.net
"""

# library
import unittest

import pytest
from requests import ConnectionError

# module
from elib_wx.avwx import exceptions, service


@pytest.mark.long
class TestService(unittest.TestCase):
    serv: service.Service

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serv = service.Service('metar')

    def test_init(self):
        """
        Tests that the Service class is initialized properly
        """
        for attr in ('rtype', 'make_err', '_extract', 'fetch'):
            self.assertTrue(hasattr(self.serv, attr))
        self.assertEqual(self.serv.rtype, 'metar')

    def test_service(self):
        """
        Tests that the base Service class has no URL and throws NotImplemented errors
        """
        if type(self.serv) == service.Service:
            with self.assertRaises(NotImplementedError):
                # noinspection PyTypeChecker
                self.serv._extract(None)
        else:
            self.assertIsInstance(self.serv.url, str)
        self.assertIsInstance(self.serv.method, str)
        self.assertIn(self.serv.method, ('GET', 'POST'))

    def test_make_err(self):
        """
        Tests that InvalidRequest exceptions are generated with the right message
        """
        key, msg = 'test_key', 'testing'
        err = self.serv.make_err(msg, key)
        err_str = f'Could not find {key} in {self.serv.__class__.__name__} response\n{msg}'
        self.assertIsInstance(err, exceptions.InvalidRequestError)
        self.assertEqual(err.args, (err_str,))
        self.assertEqual(str(err), err_str)

    def test_fetch(self):
        """
        Tests fetch exception handling
        """
        for station in ('12K', 'MAYT'):
            with self.assertRaises(exceptions.BadStationError):
                self.serv.fetch(station)
        # Should raise exception due to empty url
        with self.assertRaises(AttributeError):
            self.serv.fetch('KJFK')


class TestNOAA(TestService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serv = service.NOAA('metar')

    def test_fetch(self):
        """
        Tests that reports are fetched from NOAA ADDS
        """
        for station in ('12K', 'MAYT'):
            with self.assertRaises(exceptions.BadStationError):
                self.serv.fetch(station)
        for station in ('KJFK', 'EGLL', 'PHNL'):
            report = self.serv.fetch(station)
            self.assertIsInstance(report, str)
            self.assertTrue(report.startswith(station))


@pytest.mark.xfail(raises=ConnectionError)
def test_fetch_amo():
    """
    Tests that reports are fetched from AMO for Korean stations
    """
    serv = service.AMO('metar')
    for station in ('12K', 'MAYT'):
        with pytest.raises(exceptions.BadStationError):
            serv.fetch(station)
    for station in ('RKSI', 'RKSS', 'RKNY'):
        report = serv.fetch(station)
        assert isinstance(report, str)
        assert report.startswith(station)


class TestMAC(TestService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serv = service.MAC('metar')

    def test_fetch(self):
        """
        Tests that reports are fetched from AMO for Korean stations
        """
        for station in ('12K', 'MAYT'):
            with self.assertRaises(exceptions.BadStationError):
                self.serv.fetch(station)
        for station in ('SKBO',):
            report = self.serv.fetch(station)
            self.assertIsInstance(report, str)
            self.assertTrue(report.startswith(station))


class TestModule(unittest.TestCase):

    def test_get_service(self):
        """
        Tests that the correct service class is returned
        """
        for stations, serv in (
            (('KJFK', 'EGLL', 'PHNL'), service.NOAA),
            (('RKSI',), service.AMO),
            (('SKBO', 'SKPP'), service.MAC),
        ):
            for station in stations:
                self.assertIsInstance(service.get_service(station)(station), serv)
