# -*- coding: utf-8 -*-
"""
Module utils.py:
--------------------------
    A set of utility functions.
"""
import sys
import signal
import datetime


def signal_name(signum):
    """
    Gets the signal name.
    :param signum: The received signal code.
    :return: the signal name or 'SIG_UNKNOWN'.
    """
    try:
        return signal.Signals(signum).name
    except KeyError:
        return 'SIG_UNKNOWN'
    except ValueError:
        return 'SIG_UNKNOWN'


def get_safe_exception_string(exc_strings):
    """Ensure list of exception strings is decoded on Python 2 and joined as one string safely."""
    if sys.version_info[0] < 3:
        try:
            exc_strings = [exc.decode("utf-8") for exc in exc_strings]
        except ValueError:
            exc_strings = [exc.decode("latin-1") for exc in exc_strings]
    return ''.join(exc_strings)


_TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def utcformat(dt):
    """
    Parses dates to string in utc format.
    :param dt: data or datetime object 
    :return: string in utc format.
    """
    return dt.strftime(_TIMESTAMP_FORMAT)


def utcparse(string):
    """
    parses a string dates in utc format into a datetime object.
    :param string: string date in utc format.
    :return: a datetime object.
    """
    try:
        return datetime.datetime.strptime(string, _TIMESTAMP_FORMAT)
    except ValueError:
        # This catches any jobs remain with old datetime format
        return datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ')
