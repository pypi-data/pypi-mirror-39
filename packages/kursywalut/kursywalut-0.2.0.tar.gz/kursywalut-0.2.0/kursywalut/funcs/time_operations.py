# -*- coding: utf-8 -*-
"""Time Operations Package."""

from datetime import datetime

__author__ = 'Bart Grzybicki'


def now(return_type=None):
    """Return current time.

    Args:
        return_type (type): Optional argument, pass str() if you want
            to get string.

    Returns:
        date in datetime format or as a string.

    """
    if return_type == str():
        return str(datetime.now())
    else:
        return datetime.now()


def elapsed_time(time_start, time_end):
    """Return time difference.

    Args:
        time_start (datetime): start time.
        time_end (datetime): end time.

    Returns:
        datetime: difference between two times.

    """
    return time_end - time_start
