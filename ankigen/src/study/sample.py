from dataclasses import dataclass
from typing import Optional

from ankigen.src.study.lemmatization import Lemmatization

SINGLE_WORD_EFFORT = 30.0
MINIMUM_EFFORT = 10.0


class Sample:
    def __init__(self, text: str, source: Optional[str] = None, english: Optional[str] = None) -> None:
        self._text = text
        self._source = source
        self._english = english
        self._lemmatization = Lemmatization.from_text(text)
        self._effort = _calc_effort(self._lemmatization)

    @property
    def text(self) -> str:
        return self._text

    @property
    def source(self) -> Optional[str]:
        return self._source

    @property
    def english(self) -> Optional[str]:
        return self._english

    @property
    def lemmatization(self) -> Lemmatization:
        return self._lemmatization

    @property
    def effort(self) -> float:
        return self._effort

    def __hash__(self) -> int:
        return hash((self._text, self._source, self._english))

    def __str__(self) -> str:
        return self._text


# todo improve this
def _calc_effort(lemmatization: Lemmatization) -> float:
    length = float(len(lemmatization.lemmas))
    return max(length, (MINIMUM_EFFORT - SINGLE_WORD_EFFORT) / (MINIMUM_EFFORT - 1.0) * (length - 1.0) + SINGLE_WORD_EFFORT)
