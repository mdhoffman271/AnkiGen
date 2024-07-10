from __future__ import annotations

from typing import Iterable

from ankigen.src.language.sentence import unique_lemma_vector
from ankigen.src.study.sample_store import SampleStore


class InterestStore:
    def __init__(self, lang: str) -> None:
        self._lang = lang
        self._interests = set()

    def add_interest(self, interest: str) -> None:
        key = unique_lemma_vector(interest, self._lang)
        if key:
            self._interests.add(key)

    def add_interests(self, interests: Iterable[str]) -> None:
        for interest in interests:
            self.add_interest(interest)

    def sample_store(self, max_sample_count: int = 3) -> SampleStore:
        return SampleStore(self._lang, max_sample_count, self._interests)
