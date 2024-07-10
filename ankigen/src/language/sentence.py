import re
from typing import Iterable

from nltk.tokenize import sent_tokenize
from simplemma import is_known, text_lemmatizer  # type: ignore

LANG_LANGUAGE_MAP = {
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'et': 'estonian',
    'fi': 'finnish',
    'fr': 'french',
    'de': 'german',
    'el': 'greek',
    'it': 'italian',
    'no': 'norwegian',
    'pl': 'polish',
    'pt': 'portuguese',
    'ru': 'russian',
    'sk': 'slovene',
    'es': 'spanish',
    'sv': 'swedish',
    'th': 'turkish',
}


def iter_sentences(text: str, lang: str) -> Iterable[str]:
    yield from sent_tokenize(text, LANG_LANGUAGE_MAP[lang])


WORD_PATTERN = re.compile(r'\w+')


def iter_lemmas(text: str, lang: str) -> Iterable[str]:
    return filter(WORD_PATTERN.fullmatch, text_lemmatizer(text, lang=lang, greedy=True))


def iter_valid_lemmas(text: str, lang: str) -> Iterable[str]:
    for lemma in iter_lemmas(text, lang):
        if is_valid_lemma(lemma, lang):
            yield lemma


UniqueLemmaVector = tuple[str, ...]


def unique_lemma_vector(text: str, lang: str) -> UniqueLemmaVector:
    return tuple(sorted(iter_valid_lemmas(text, lang)))


def is_valid_lemma(text: str, lang: str) -> bool:
    return is_known(text, lang)
