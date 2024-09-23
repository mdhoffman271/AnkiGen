import re
from threading import Lock
from typing import Iterable, Optional, Self

# These dependencies are expensive, and should be used only by the active context.
from nltk.tokenize import sent_tokenize
from simplemma import is_known, text_lemmatizer  # type: ignore


# Prevent anyone else from modifying the context while this lock is held.
class ContextLock:
    def __init__(self, lock: Lock, timeout: float = 1.0) -> None:
        if not lock.acquire(timeout=timeout):
            raise RuntimeError('unable to acquire unique lock on context')

        self._lock: Optional[Lock] = lock

    def release(self) -> None:
        if self._lock is None:
            raise RuntimeError('cannot release lock twice')
        self._lock.release()
        self._lock = None

    def __enter__(self) -> Self:
        return self

    def __exit__(self, _, __, ___) -> None:
        self.release()


class _Context:
    def __init__(self) -> None:
        self._lang = 'en'
        self._lock = Lock()

    # Acquire a lock on this context, preventing anyone else from doing the same.
    def lock(self, lang: Optional[str]) -> ContextLock:
        result = ContextLock(self._lock)
        if lang is not None:
            self._set_lang(lang)
        return result

    @property
    def lang(self) -> str:
        return self._lang

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

    def _set_lang(self, lang: str) -> None:
        if lang not in _LANG_LANGUAGE_MAP:
            raise ValueError(f'unrecognized lang: {lang}')
        self._lang = lang


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
