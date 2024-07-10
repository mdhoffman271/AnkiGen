from typing import Iterable

from ankigen.src.language.sentence import UniqueLemmaVector
from ankigen.src.study.sample import Sample


class SampleStore:
    def __init__(self, lang: str, max_sample_count: int, interests: Iterable[UniqueLemmaVector]) -> None:
        self._lang = lang
        self._max_sample_count = max_sample_count
        self._interest_samples_map: dict[UniqueLemmaVector, list[Sample]] = {interest: [] for interest in interests}

    def _append_sample(self, samples: list[Sample], sample: Sample) -> None:
        samples.append(sample)
        while len(samples) > self._max_sample_count:
            i = 0
            for j in range(1, len(samples)):
                if samples[j].effort > samples[i].effort:
                    i = j
            samples.pop(i)

    def add_sample(self, sample: Sample) -> None:
        if sample.lang != self._lang:
            return

        for interest, samples in self._interest_samples_map.items():
            sample_lemmas = sample.get_unique_lemmas()
            for lemma in interest:
                if lemma not in sample_lemmas:
                    break
            else:
                self._append_sample(samples, sample)

    def add_samples(self, samples: Iterable[Sample]) -> None:
        for sample in samples:
            self.add_sample(sample)

    def iter_items(self) -> Iterable[tuple[UniqueLemmaVector, Sample]]:
        for interest, samples in self._interest_samples_map.items():
            for sample in samples:
                yield interest, sample

    def iter_interests(self) -> Iterable[UniqueLemmaVector]:
        return self._interest_samples_map.keys()

    def iter_samples(self) -> Iterable[Sample]:
        for samples in self._interest_samples_map.values():
            yield from samples
