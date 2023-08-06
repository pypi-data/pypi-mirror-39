"""
Language
---------

This module contains `Language` class which is used for detecting and selecting languages for future processing
"""

from langdetect import detect as _detect

from .settings import Defaults


class Language:
    """
    Attributes
    -----------
    lang: language in ISO format
    title: language full title

    Examples
    ---------
    >>> lang = Language(text='Съешь ещё этих мягких французских булок')
    >>> print(lang.title)
    russian
    """

    def __init__(self, lang: str = '', text: str = ''):
        self.lang = lang or self.detect(text)
        self.title = Defaults.langs.get(self.lang, '')

    def __repr__(self) -> str:
        if self.title:
            return self.title
        else:
            return '[unsupported] %s' % self.lang

    @property
    def is_supported(self) -> bool:
        if len(self.lang) < 2:
            return False
        if self.lang[:2] not in Defaults.langs.keys():
            return False
        return True

    @staticmethod
    def detect(text: str) -> str:
        return _detect(text)[:2] if text else ''
