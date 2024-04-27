from __future__ import annotations

from dataclasses import dataclass
from heapq import heappush, heappushpop
from typing import Iterable

from ankigen.src.sample import Sample
from ankigen.src.sentence import iter_valid_lemmas


class InterestStore:
    @dataclass
    class SampleWrapper:
        sample: Sample

        def __lt__(self, other: InterestStore.SampleWrapper) -> bool:
            return other.sample.effort < self.sample.effort

    INTEREST = tuple[str, ...]
    HEAP = list[SampleWrapper]

    def __init__(self, lang: str, max_samples: int = 4) -> None:
        self._lang = lang
        self._max_samples = max_samples
        self._interest_heap_map: dict[InterestStore.INTEREST, InterestStore.HEAP] = dict()

    def add_interest(self, interest: str) -> None:
        key = tuple(sorted(iter_valid_lemmas(interest, self._lang)))
        if key not in self._interest_heap_map:
            self._interest_heap_map[key] = list()

    def add_sample(self, sample: Sample) -> None:
        for interest, heap in self._interest_heap_map.items():
            for lemma in interest:
                if lemma not in sample.unique_lemmas:
                    break
            else:
                value = InterestStore.SampleWrapper(sample)
                if len(heap) >= self._max_samples:
                    heappushpop(heap, value)
                else:
                    heappush(heap, value)

    def add_samples(self, samples: Iterable[Sample]) -> None:
        for sample in samples:
            self.add_sample(sample)

    def iter_items(self) -> Iterable[tuple[InterestStore.INTEREST, Sample]]:
        for interest, heap in self._interest_heap_map.items():
            for wrapper in heap:
                yield interest, wrapper.sample
