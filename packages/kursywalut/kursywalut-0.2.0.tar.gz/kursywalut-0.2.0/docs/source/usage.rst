=====
Usage
=====

Podstawowe użycie::

Jako osobna aplikacja::

    (venv) $ kursywalut
    ##################
    $ KursyWalut 0.2 $
    ##################

    Pobieram dane... FOREX
    OK
    Pobieram dane... NBP
    OK

    FOREX	kupno	sprzedaż

    DATA	Dziś, 20.12.2018 09:43
    EUR	4,2800	4,2825
    CHF	3,7769	3,7799
    GBP	4,7404	4,2825
    USD	3,7447	3,7472

    NBP	kurs średni

    DATA	nr 246/A/NBP/2018 z dnia 19-12-2018
    EUR	4,2846
    CHF	3,7875
    GBP	4,7607
    USD	3,7619


W swoim programie::

    (venv) $ ipython
    Python 3.6.7 (default, Oct 22 2018, 11:32:17)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 7.2.0 -- An enhanced Interactive Python. Type '?' for help.

    In [1]: import kursywalut

    In [2]: moneypl = kursywalut.handlers.MoneyPlHandler()

    In [3]: data = moneypl.get_moneypl()
    Pobieram dane... FOREX
    OK
    Pobieram dane... NBP
    OK

    In [4]: print(data)
    OrderedDict([('FOREX', OrderedDict([('DATA', 'Dziś, 20.12.2018 09:59'), ('EUR', ['4,2808', '4,2833']), ('CHF', ['3,7784', '3,7813']), ('GBP', ['4,7429', '4,2833']), ('USD', ['3,7453', '3,7478'])])), ('NBP', OrderedDict([('DATA', 'nr 246/A/NBP/2018 z dnia 19-12-2018'), ('EUR', '4,2846'), ('CHF', '3,7875'), ('GBP', '4,7607'), ('USD', '3,7619')]))])
