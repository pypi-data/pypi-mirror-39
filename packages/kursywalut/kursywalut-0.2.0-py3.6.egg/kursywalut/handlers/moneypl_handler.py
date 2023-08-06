# -*- coding: utf-8 -*-
"""money.pl handler module.

Prepared requests are being passed to the get_webpage() method
inherited from GenericHandler class. In the next receved response is passed
over to the MoneyPlParser().parse() method. In the last step parsed data
is returned by the get_moneypl() method.

"""

import logging

from ..funcs.time_operations import now, elapsed_time
from ..parsers.moneypl_parser import MoneyPlParser
from .generic_handler import GenericHandler


logger = logging.getLogger(__name__)


class MoneyPlHandler(GenericHandler):
    """MoneyPlHandler class.

    Attributes:
        site_mapping (dict): A dict containing website mapping.
        page_list (list): A list of string containing responses from websites.
        page (str): data retrieved from website.
        url (str): URL to retrieve data from.

        url_forex (str): URL for FOREX currency exchange.
        url_nbp (str): URL for NBP currency exchange.

    """

    def __init__(self):
        """Initialization method."""
        super(MoneyPlHandler, self).__init__(None)
        self.site_mapping = {
            'FOREX': 'https://www.money.pl/pieniadze/forex/',
            'NBP': 'https://www.money.pl/pieniadze/nbp/srednie/',
        }
        self.url_forex = self.site_mapping['FOREX']
        self.url_nbp = self.site_mapping['NBP']
        self.page_list = []

    def _get_forex(self):
        """_get_forex method.

        Send request for FOREX data and add parsed data to the list.

        """
        logger.debug(self._get_forex.__name__)
        self.url = self.url_forex
        self.get_webpage()
        self.page_list.append(self.page)
        self.parser = MoneyPlParser(self, self.site_mapping)

    def _get_nbp(self):
        """_get_nbp method.

        Send request for NBP data and add parsed data to the list.

        """
        logger.debug(self._get_nbp.__name__)
        self.url = self.url_nbp
        self.get_webpage()
        self.page_list.append(self.page)

    def get_moneypl(self):
        """get_moneypl method.

        Send requests for FOREX and NBP data and parse both responses.

        Returns:
            Parsed data as OrderedDict.

        """
        logger.debug(self.get_moneypl.__name__)
        self.page_list = []
        start = now()
        self._get_forex()
        self._get_nbp()
        self.download_time = elapsed_time(start, now())
        start = now()
        self.data_parsed = self.parser.parse()
        self.parse_time = elapsed_time(start, now())
        logger.debug('self.data_parsed={}'.format(self.data_parsed))

        return self.data_parsed
