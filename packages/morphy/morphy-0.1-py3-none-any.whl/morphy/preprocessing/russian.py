from typing import List, Union, NamedTuple

from cached_property import cached_property
from spacy.lang import ru
from spacy.tokens import Doc

from .multilang import MultiLang
from .types import TokenList
from ..interfaces import Token


class Russian(MultiLang):
    """ Inherited from `Base`, based on mix of `pymorphy2` and `spacy` processing for Russian

    Attributes
    ----------
    lemmatizer: `pymorphy2` processor for Russian
    enable_wiki_ner: Set `True` by default because `spacy` has no model for Russian
    """

    def __init__(self, **kwargs):
        super().__init__('ru', **kwargs)
        self.lemmatizer = ru.RussianLemmatizer()
        self.enable_wiki_ner = True

    @cached_property
    def processor(self) -> ru.Russian:
        """ For Russian there is no trained `spacy` model, therefore it is loaded by calling class
        `spacy.lang.ru.Russian` and only `sbd` (sentence tokenization) pipe is used. Lemmatization uses a package
        `pymorphy2`, which is the best package of NLP for the Russian language to date. """

        result = ru.Russian()
        result.add_pipe(result.create_pipe('sbd'))
        return result

    def extract_noun_phrases(self, text: Union[str, List[str]] = None, doc: Doc = None) -> TokenList:
        """ Not implemented """

        return []

    def extract_tokens(self, text: Union[str, List[str]] = None, doc: Doc = None) -> TokenList:
        """ Tokenize input text, marks tokens that passed filtering """

        doc = doc or self.parse_doc(text)

        if not doc:
            return []

        result = [Token(token.text, is_stop=token.is_stop) for token in doc]

        for i, token in enumerate(result):
            token.id = i
            parsed_word = self.parse_ru_word(token.text)
            token.lemma = parsed_word.lemma
            token.tag = parsed_word.pos

            if (
                token.tag in self.allowed_pos_tags and
                not token.is_stop and
                len(token.lemma) >= self.min_token_len and
                token.text.isalnum()
            ):
                token.matches = True

        return result

    def normalize_tag(self, tag) -> str:
        """ Converts `pymorphy2` POS tag type to string """

        return self.lemmatizer.normalize_univ_pos(tag)

    class RuWord(NamedTuple):
        pos: str
        lemma: str

    def parse_ru_word(self, word: str) -> RuWord:
        """ Special morphological parser for russian language """

        pos = 'NOUN'
        # TODO: Proper warning suppression
        morph = self.lemmatizer._morph.parse(word)[0]
        if 'LATN' in morph.tag or 'NUMB' in morph.tag:
            if 'NUMB' in morph.tag:
                pos = 'NUM'
            lemma = word.lower()
        elif hasattr(morph.tag, 'POS'):
            pos = self.normalize_tag(morph.tag.POS) or pos
            lemma = morph.normal_form
        else:
            lemma = word

        return self.RuWord(pos, lemma)
