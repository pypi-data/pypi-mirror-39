"""
Exceptions
----------

This module defines `morphy` custom exceptions.
"""


class MorphyError(Exception):
    """ Common `morphy` exception """

    pass


class LangError(Exception):
    """ Exception, that can be raised when text of not supported language is processing """

    def __init__(self, message: str = ''):
        self.message = message or 'Selected language is not supported'
