# -*- coding: utf-8 -*-
"""String Operations Package."""

import six

__author__ = 'Bart Grzybicki'


def _to_unicode(value):
    """Convert value to unicode.

    Args:
        value (str): Value to be converted to unicode.

    Returns:
        string (Python 3) or unicode (Python 2).

    """
    return six.text_type(value)


def print_unicode(string):
    """Print unicode function.

    Prints string (Python 3) or string converted to unicode (Python 2).

    """
    print(_to_unicode(string))
