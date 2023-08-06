from typing import NamedTuple, List, Dict


class _Defaults(NamedTuple):
    """ Default settings for preprocessing and language classes """

    allowed_pos_tags: List[str] = ['ADJ', 'NOUN', 'PROPN', 'VERB', 'NUM']
    max_phrase_len: int = 4
    min_phrase_len: int = 2
    min_sent_len: int = 5
    min_token_len: int = 3
    enable_wiki_ner: bool = True
    abbrev_except: List[str] = ['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'i.e', 'e.g', 'etc', 'p.s', 'n.b']
    langs: Dict = {
        'en': 'english',
        'de': 'german',
        'es': 'spanish',
        'pt': 'portuguese',
        'fr': 'french',
        'it': 'italian',
        'nl': 'dutch',
        'ru': 'russian'
    }


Defaults = _Defaults()
