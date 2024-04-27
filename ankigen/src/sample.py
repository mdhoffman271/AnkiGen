from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import List, Optional

from ankigen.src.sentence import iter_lemmas

SINGLE_WORD_EFFORT = 30.0
MINIMUM_EFFORT = 10.0


@dataclass(frozen=True)
class Sample:
    lang: str
    text: str
    url: Optional[str] = None

    @property
    @cache
    def all_lemmas(self) -> List[str]:
        return list(iter_lemmas(self.text, self.lang))

    @property
    @cache
    def unique_lemmas(self) -> set[str]:
        return set(self.all_lemmas)

    @property
    @cache
    def effort(self) -> float:
        length = float(len(self.all_lemmas))
        return max(length, (MINIMUM_EFFORT - SINGLE_WORD_EFFORT) / (MINIMUM_EFFORT - 1.0) * (length - 1.0) + SINGLE_WORD_EFFORT)
