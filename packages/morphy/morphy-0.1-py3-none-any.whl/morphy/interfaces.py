"""
Representation of texts processed after NLP
--------------------------------------------

This module defines main text containers, which represent common information about item of selected level
"""

from typing import List, Dict, Union, Iterator


class Sentence:
    """ Is used when task requires sentence structured text.

    Attributes
    ----------
    matches: If True, current sentence passed filtering at sentence segmentation stage

    Examples
    --------
    >>> sent = Sentence('This is a small test sentence')
    """

    def __init__(self, text: str, _id: int = None, matches: bool = False):
        self.id = _id
        self.text = text
        self.matches = matches

        self.tokens = None  # type: List[Token]

    def __repr__(self):
        return '[%s] %s' % ('+' if self.matches else '-', ' '.join(self.text.split()))

    def __iter__(self) -> Union[Iterator, None]:
        return iter(self.tokens) if self.tokens else None

    def save(self):
        return {'id': self.id, 'text': self.text, 'matches': self.matches,
                'tokens': [t.save() for t in self.tokens] if self.tokens else []}

    @classmethod
    def load(cls, data: Dict) -> 'Sentence':
        sent = cls(data['text'], data['id'], data['matches'])
        sent.tokens = [Token.load(t) for t in data['tokens']] if data['tokens'] else None
        return sent


class Token:
    """ Container for token (word, entity or phrase) metadata.

    Attributes
    ----------
    text: Original word form from input text
    lemma: Normal word form
    tag: Word POS tag or category (for entity and phrase)
    is_stop: If True, token belongs to so called `stop words`
    """

    def __init__(self, text: str, id: int = None, lemma: str = '', tag: str = '', is_stop: bool = False,
                 matches: bool = False):
        self.id = id
        self.text = text
        self.lemma = lemma
        self.tag = tag
        self.is_stop = is_stop
        self.matches = matches

    def __repr__(self):
        return '[%s] %s -> %s (%s)' % ('+' if self.matches else '-', self.text, self.lemma, self.tag)

    def save(self):
        return {'id': self.id, 'text': self.text, 'lemma': self.lemma, 'tag': self.tag, 'is_stop': self.is_stop,
                'matches': self.matches}

    @classmethod
    def load(cls, data: Dict) -> 'Token':
        return cls(**data)
