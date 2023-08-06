# -*- coding: utf-8 -*-

"""Tests for `interface` package."""

import pytest
import mock

from requests.exceptions import RequestException

from kursywalut.interface import interface

DATA = {'FOREX': {'CHF': ['3,8007', '3,8107'],
                  'DATA': 'Dziś, 16.12.2018 11:32',
                  'EUR': ['4,2864', '4,2964'],
                  'GBP': ['4,7698', '4,2964'],
                  'USD': ['3,7924', '3,8024']},
        'NBP': {'CHF': '3,8202',
                'DATA': 'nr 243/A/NBP/2018 z dnia 14-12-2018',
                'EUR': '4,3021',
                'GBP': '4,7940',
                'USD': '3,8095'}}


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """

    interface.get_moneypl = mock.MagicMock(return_value=DATA)

    return interface.get_moneypl()


def test_response(response, expected=DATA):
    """Sample pytest test function with the pytest fixture as an argument."""

    assert response == expected
