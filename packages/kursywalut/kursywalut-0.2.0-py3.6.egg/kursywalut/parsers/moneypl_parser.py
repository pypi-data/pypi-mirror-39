# -*- coding: utf-8 -*-
"""money.pl parser module.

Currency data is retireved from the following websites:

self.site_mapping = {
    'FOREX': 'https://www.money.pl/pieniadze/forex/',
    'NBP': 'https://www.money.pl/pieniadze/nbp/srednie/',
}

"""

from collections import OrderedDict

from lxml import html

from ..funcs.string_operations import _to_unicode


class MoneyPlParser(object):
    """MoneyPlParser class.

    Classs for parsing retried currency exchange data.

    Attributes:
        moneypl_handler (object): instance of MoneyPlHandler() class.
        currency (OrderedDict): dictionary containing all currency
            exchange data.

    """

    def __init__(self, moneypl_handler, site_mapping):
        """Initialization metod.

        Args:
            moneypl_handler (object): instance of MoneyPlHandler() class.
            site_mapping (dict): A dict containing website mapping.
        """
        self.moneypl_handler = moneypl_handler
        self.currency = OrderedDict()
        for key, value in site_mapping.items():
            if value == self.moneypl_handler.url:
                self.currency[key] = {}

    def _get_text(self):
        """Return parsed data or a list with parsed data."""
        if self.moneypl_handler.page_list is not None:
            return self.moneypl_handler.page_list
        else:
            return self.moneypl_handler.page

    def parse(self):
        """Parse xpath method.

        Returns:
            Dictionary (OrderedDict) with currency exchange data.

        """
        page_raw = self._get_text()
        if type(page_raw) == list:
            # FOREX
            page = page_raw[0]
            tree = html.fromstring(page)

            post_date_forex = \
                tree.xpath('//span[@class="xqiouj-5 kFhDeu"]/text()')[0]

            eur_pln_buy = tree.xpath(
                '//*[@id="app"]/div/div[7]/div/div[2]/div/main/div/section[1]\
                /div[2]/div/div/div/div[1]/div[2]/div[4]/div/div[2]/div')[
                0].text_content()
            eur_pln_sell = tree.xpath(
                '//*[@id="app"]/div/div[7]/div/div[2]/div/main/div/section[1]\
                /div[2]/div/div/div/div[1]/div[2]/div[4]/div/div[3]/div')[
                0].text_content()

            chf_pln_buy = tree.xpath(
                '//*[@id="app"]/div/div[7]/div/div[2]/div/main/div/section[1]\
                /div[2]/div/div/div/div[1]/div[2]/div[3]/div/div[2]/div')[
                0].text_content()
            chf_pln_sell = tree.xpath(
                '//*[@id="app"]/div/div[7]/div/div[2]/div/main/div/section[1]\
                /div[2]/div/div/div/div[1]/div[2]/div[3]/div/div[3]/div')[
                0].text_content()

            gbp_pln_buy = tree.xpath(
                '//*[@id="app"]/div/div[7]/div/div[2]/div/main/div/section[1]\
                /div[2]/div/div/div/div[1]/div[2]/div[5]/div/div[2]/div')[
                0].text_content()
            gbp_pln_sell = tree.xpath(
                '//*[@id="app"]/div/div[7]/div/div[2]/div/main/div/section[1]\
                /div[2]/div/div/div/div[1]/div[2]/div[4]/div/div[3]/div')[
                0].text_content()

            usd_pln_buy = tree.xpath(
                '//*[@id="app"]/div/div[7]/div/div[2]/div/main/div/section[1]\
                /div[2]/div/div/div/div[1]/div[2]/div[6]/div/div[2]/div')[
                0].text_content()
            usd_pln_sell = tree.xpath(
                '//*[@id="app"]/div/div[7]/div/div[2]/div/main/div/section[1]\
                /div[2]/div/div/div/div[1]/div[2]/div[6]/div/div[3]/div')[
                0].text_content()

            # NBP - average
            page = page_raw[1]
            tree = html.fromstring(page)
            post_date_nbp = \
                tree.xpath('//span[@class="sc-1fexh53-0 gVFZcf"]/text()')[0]

            eur_nbp_avg = tree.xpath(
                '//*[@id="app"]/div/div[7]/div/div[2]/div/main/div/div[5]/div/\
                div/div[1]/div[2]/div[8]/div/div[3]/div')[
                0].text_content()
            chf_nbp_avg = tree.xpath(
                '//*[@id="app"]/div/div[7]/div/div[2]/div/main/div/div[5]/div/\
                div/div[1]/div[2]/div[10]/div/div[3]/div')[
                0].text_content()
            gbp_nbp_avg = tree.xpath(
                '//*[@id="app"]/div/div[7]/div/div[2]/div/main/div/div[5]/div/\
                div/div[1]/div[2]/div[11]/div/div[3]/div')[
                0].text_content()
            usd_nbp_avg = tree.xpath(
                '//*[@id="app"]/div/div[7]/div/div[2]/div/main/div/div[5]/div/\
                div/div[1]/div[2]/div[2]/div/div[3]/div')[
                0].text_content()

        else:
            page = page_raw

        self.currency['FOREX'] = OrderedDict()
        self.currency['NBP'] = OrderedDict()
        self.currency['FOREX']['DATA'] = _to_unicode(post_date_forex)
        self.currency['FOREX']['EUR'] = [eur_pln_buy, eur_pln_sell]
        self.currency['FOREX']['CHF'] = [chf_pln_buy, chf_pln_sell]
        self.currency['FOREX']['GBP'] = [gbp_pln_buy, gbp_pln_sell]
        self.currency['FOREX']['USD'] = [usd_pln_buy, usd_pln_sell]
        self.currency['NBP']['DATA'] = post_date_nbp
        self.currency['NBP']['EUR'] = eur_nbp_avg
        self.currency['NBP']['CHF'] = chf_nbp_avg
        self.currency['NBP']['GBP'] = gbp_nbp_avg
        self.currency['NBP']['USD'] = usd_nbp_avg

        return self.currency
