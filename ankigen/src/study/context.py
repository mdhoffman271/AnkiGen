import re
from typing import Iterable

from nltk.tokenize import sent_tokenize
from simplemma import is_known, text_lemmatizer  # type: ignore


class _Context:
    def __init__(self) -> None:
        self._lang = 'en'

    @property
    def lang(self) -> str:
        return self._lang

    @lang.setter
    def lang(self, lang: str) -> None:
        if lang not in _LANG_LANGUAGE_MAP:
            raise ValueError(f'unrecognized lang: {lang}')
        self._lang = lang

    @property
    def language(self) -> str:
        return _LANG_LANGUAGE_MAP[self._lang]

    def iter_lemmas(self, text: str) -> Iterable[str]:
        lemmas = text_lemmatizer(text, lang=self._lang, greedy=True)
        lemmas = filter(_WORD_PATTERN.fullmatch, lemmas)  # Remove non-words, like punctuation.
        lemmas = filter(lambda w: is_known(w, self._lang), lemmas)  # Remove invalid words.
        return lemmas

    def iter_sentences(self, text: str) -> Iterable[str]:
        yield from sent_tokenize(text, self.language)


# Create a single static instance.
# There can only be one at a time.
ActiveContext = _Context()


_WORD_PATTERN = re.compile(r'\w+')
_LANG_LANGUAGE_MAP = {
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
