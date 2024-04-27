
from dataclasses import dataclass
from functools import cache
from typing import List, Optional

from simplemma import text_lemmatizer  # type: ignore

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
        return text_lemmatizer(self.text, lang=self.lang, greedy=True)

    @property
    @cache
    def unique_tokens(self) -> set[str]:
        return set(self.all_tokens)

    @property
    @cache
    def effort(self) -> float:
        length = float(len(self.all_tokens))
        return max(length, (MINIMUM_EFFORT - SINGLE_WORD_EFFORT) / (MINIMUM_EFFORT - 1.0) * (length - 1.0) + SINGLE_WORD_EFFORT)
