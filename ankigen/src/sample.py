
from dataclasses import dataclass
from functools import cache
from typing import List, Optional

from ankigen.src.sentence import iter_words

SINGLE_WORD_EFFORT = 30.0
MINIMUM_EFFORT = 10.0


@dataclass(frozen=True)
class Sample:
    lang: str
    text: str
    url: Optional[str] = None

    @property
    @cache
    def all_tokens(self) -> List[str]:
        return list(iter_words(self.text, self.lang))

    @property
    @cache
    def unique_tokens(self) -> set[str]:
        return set(self.all_tokens)

    @property
    @cache
    def effort(self) -> float:
        length = float(len(self.all_tokens))
        return max(length, (MINIMUM_EFFORT - SINGLE_WORD_EFFORT) / (MINIMUM_EFFORT - 1.0) * (length - 1.0) + SINGLE_WORD_EFFORT)
