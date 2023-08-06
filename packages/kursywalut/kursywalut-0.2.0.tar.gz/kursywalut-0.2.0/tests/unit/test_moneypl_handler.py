# -*- coding: utf-8 -*-

"""Tests for MoneyPlHandler class."""

import mock

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


class TestMoneyPlHandler(object):
    """
    MoneyPlHandler class tests.
    """

    # @mock.patch('kursywalut.handlers.moneypl_handler.MoneyPlHandler')
    def test_get_moneypl(self, expected=DATA):
        """Sample pytest test function with the pytest fixture as an argument."""
        with mock.patch(
            'kursywalut.handlers.moneypl_handler.MoneyPlHandler') as MockHandler:
            MockHandler.return_value.get_moneypl.return_value = DATA
            # mock_MoneyPlHandler._get_forex = mock.ANY
            handler = MockHandler()
            request = handler.get_moneypl()

            assert request == expected
            MockHandler.assert_called()
