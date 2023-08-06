# -*- coding: utf-8 -*-
"""
Module exceptions.py:
--------------------------
    A set of Simple-Queue custom exceptions.
"""


class StopRequested(Exception):
    """An exception that is raised when the worker is asked to be stopped abruptly.
    """
    pass
