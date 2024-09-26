from __future__ import annotations

import re
from abc import ABC, abstractmethod
from threading import Lock
from typing import Iterable

# These dependencies are expensive, and should be used only by the active context.
from nltk.tokenize import sent_tokenize
from simplemma import is_known, text_lemmatizer  # type: ignore

# Prevent creating another context or modifying the active lang while this lock is held.
_CONTEXT_LOCK = Lock()
_ACTIVE_LANG = 'en'


class Context:
    def __init__(self, lang: str, timeout: float = 1.0) -> None:
        self._lang = lang
        self._timeout = timeout

    # Using the ActiveContext after __exit__ is undefined behavior.
    def __enter__(self) -> ActiveContext:
        if not _CONTEXT_LOCK.acquire(timeout=self._timeout):
            raise RuntimeError('unable to acquire unique lock on context')
        global _ACTIVE_LANG
        _ACTIVE_LANG = self._lang
        return _ActiveContextImpl()

    def __exit__(self, _, __, ___) -> None:
        _CONTEXT_LOCK.release()


class ActiveContext(ABC):
    @property
    @abstractmethod
    def lang(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def language(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def iter_lemmas(self, text: str) -> Iterable[str]:
        raise NotImplementedError()

    @abstractmethod
    def iter_sentences(self, text: str) -> Iterable[str]:
        raise NotImplementedError()


class _ActiveContextImpl(ActiveContext):
    @property
    def lang(self) -> str:
        return _ACTIVE_LANG

    @property
    def language(self) -> str:
        return _LANG_LANGUAGE_MAP[self.lang]

    def iter_lemmas(self, text: str) -> Iterable[str]:
        lemmas = text_lemmatizer(text, lang=self.lang, greedy=True)
        lemmas = filter(_WORD_PATTERN.fullmatch, lemmas)  # Remove non-words, like punctuation.
        lemmas = filter(lambda w: is_known(w, self.lang), lemmas)  # Remove invalid words.
        return lemmas

    def iter_sentences(self, text: str) -> Iterable[str]:
        yield from sent_tokenize(text, self.language)


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
