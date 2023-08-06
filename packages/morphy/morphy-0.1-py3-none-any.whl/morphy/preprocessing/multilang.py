"""
Representation of NLP classes
------------------------------

This module defines natural language processors for all supported languages (english, german and russian are supported
currently).

`Base` class represents common methods for text processing: sentence segmentation, tokenization, NER and noun phrases
extraction; abstract class for `English`, `German` and `Russian`.

`Processors` class is used to load all supported processors.
"""

from string import punctuation, whitespace, digits
from typing import List, Union, Callable

import nltk
import spacy
import spacy.language
import spacy.tokens
from cached_property import cached_property

from .types import TokenList, WordList
from ..errors import LangError, MorphyError
from ..interfaces import Token, Sentence
from ..lang import Language
from ..settings import Defaults


class MultiLang:
    """ Represents common methods for text processing: sentence segmentation, tokenization, NER and noun phrases
    extraction

    Attributes
    ----------
    lang: Current processor language
    allowed_pos_tags: List of allowed token POS tags
    max_phrase_len: Max number of words in phrase in order for it to pass filtering
    min_phrase_len: Min number of words in phrase (threshold) in order for it to pass filtering
    min_sent_len: Min number of words in sentence in order for it to pass filtering
    min_token_len: Min number of characters in word in order for it to pass filtering
    enable_wiki_ner: If true, NER will be processed using model, trained on `wikipedia` corpus, otherwise, on model
                    for current `lang`
    abbrev_except: List of abbreviations the sentence segmenter should ignore
    """

    def __init__(self, lang: str, allowed_pos_tags: WordList = None, max_phrase_len: int = None,
                 min_phrase_len: int = None, min_sent_len: int = None, min_token_len: int = None,
                 enable_wiki_ner: bool = False, abbrev_except: WordList = None):
        self.lang = Language(lang)
        if not self.lang.is_supported:
            raise LangError

        self.allowed_pos_tags = allowed_pos_tags or Defaults.allowed_pos_tags
        self.max_phrase_len = max_phrase_len or Defaults.max_phrase_len
        self.min_phrase_len = min_phrase_len or Defaults.min_phrase_len
        self.min_sent_len = min_sent_len or Defaults.min_sent_len
        self.min_token_len = min_token_len or Defaults.min_token_len
        self.enable_wiki_ner = enable_wiki_ner or Defaults.enable_wiki_ner
        self.abbrev_except = abbrev_except or Defaults.abbrev_except

    @cached_property
    def processor(self) -> spacy.language.Language:
        """ Loads `spacy` model for specific language """

        try:
            return spacy.load(self.lang.lang, disable=['ner']) if self.enable_wiki_ner else spacy.load(self.lang.lang)
        except FileNotFoundError as e:
            raise MorphyError(e)

    @cached_property
    def ner(self) -> spacy.language.Language:
        """ Loads `spacy` model `xx` (multilingual, trained on `wikipedia` corpus)

        Notes
        ------
        NER is processed by pipe `ner` of the current language, or by calling `spacy.lang.xx` model
        (see: https://spacy.io/usage/models#multi-language). It is not possible to add pipe 'ner' from `xx` model
        to other models.
        """

        try:
            return spacy.load('xx') if self.enable_wiki_ner else None
        except FileNotFoundError as e:
            raise MorphyError(e)

    @cached_property
    def sent_tokenizer(self) -> Union[spacy.tokens.Doc, Callable[[str], List[str]]]:
        """ Loads and customizes `nltk` sentence segmenter for respecting custom abbreviations """

        sentence_tokenizer = nltk.data.load('tokenizers/punkt/%s.pickle' % self.lang.title)
        if self.abbrev_except:
            sentence_tokenizer._params.abbrev_types.update(self.abbrev_except)
        return sentence_tokenizer.tokenize

    def parse_doc(self, text: str) -> spacy.tokens.Doc:
        """ Calls `spacy` processor for current language on `text` """

        try:
            doc = self.processor(text) if self.processor and text else None
        except IndexError:
            doc = None
        return doc

    def extract_noun_phrases(self, text: str = None, doc: spacy.tokens.Doc = None) -> TokenList:
        """ Extract noun phrases (chunks) from input text """

        doc = doc or self.parse_doc(text)

        if not doc:
            return []

        phrases_list = [Token(chunk.text, lemma=chunk.lemma_, tag='phrase') for chunk in doc.noun_chunks
                        if len(chunk.text.split()) in range(self.min_phrase_len, self.max_phrase_len)]

        result = list()
        processed_chunk_list = list()

        for i, phrase in enumerate(phrases_list):
            phrase.id = i
            phrase.text = phrase.text.strip(punctuation + whitespace)
            if phrase.text not in processed_chunk_list:
                processed_chunk_list.append(phrase.text)
                result.append(phrase)
        return result

    def extract_named_entities(self, text: str = None, doc: spacy.tokens.Doc = None) -> TokenList:
        """ NER (named-entity recognition for input text """

        if self.ner is not None:
            doc = self.ner(text)

        doc = doc or self.parse_doc(text)

        if not doc:
            return []

        result = list()
        processed_entity_list = list()

        res = [Token(ent.text, tag=ent.label_) for ent in doc.ents]
        for i, entity in enumerate(res):
            entity.id = i
            entity.text = entity.text.strip(punctuation + whitespace)
            if len(entity.text) >= self.min_token_len and entity.text[0].isupper():
                if entity.text not in processed_entity_list:
                    processed_entity_list.append(entity.text)
                    result.append(entity)
        return result

    def extract_tokens(self, text: str = None, doc: spacy.tokens.Doc = None) -> TokenList:
        """ Tokenize input text, marks tokens that passed filtering """

        doc = doc or self.parse_doc(text)

        if not doc:
            return []

        result = [
            Token(token.text, tag=token.pos_, lemma=token.lemma_.lower(), is_stop=token.is_stop)
            for token in self.processor.tagger(doc)
        ]

        for token in result:
            if (
                    token.tag in self.allowed_pos_tags and
                    not token.is_stop and
                    len(token.lemma) >= self.min_token_len and
                    token.text.isalnum()
            ):
                token.matches = True

        return result

    def extract_sentences(self, text: str = None) -> List['Sentence']:
        """ Segments input text into sentences, marks invalid sentences """

        result = list()
        for i, sent_text in enumerate(self.sent_tokenizer(text)):
            sent = Sentence(sent_text, i)
            cleaned_sent = ' '.join(sent.text.split())
            for elem in [punctuation, digits]:
                cleaned_sent = cleaned_sent.translate(str.maketrans('', '', elem))
            if cleaned_sent and \
                    len([el for el in cleaned_sent.split() if len(el) >= self.min_token_len]) > self.min_sent_len:
                sent.matches = True
            if sent.matches:
                sent.tokens = self.extract_tokens(sent.text)
            result.append(sent)

        return result
