from typing import Iterable

from ankigen.src.language.sentence import UniqueLemmaVector
from ankigen.src.study.interest import Interest
from ankigen.src.study.sample import Sample


class SampleStore:
    def __init__(self, max_sample_count: int, interests: Iterable[Interest]) -> None:
        self._max_sample_count = max_sample_count
        self._interest_samples_map: dict[Interest, list[Sample]] = {interest: [] for interest in interests}

    def add_sample(self, sample: Sample) -> None:
        sample_lemmas = sample.get_unique_lemmas()
        # todo this is slow, can be improved
        for interest, samples in self._interest_samples_map.items():
            if interest.lang == sample.lang:
                for lemma in interest.lemmas:
                    if lemma not in sample_lemmas:
                        break
                else:
                    self._append_sample(samples, sample)

    def _append_sample(self, samples: list[Sample], sample: Sample) -> None:
        samples.append(sample)
        while len(samples) > self._max_sample_count:
            i = 0
            for j in range(1, len(samples)):
                if samples[j].effort > samples[i].effort:
                    i = j
            samples.pop(i)

    def add_samples(self, samples: Iterable[Sample]) -> None:
        for sample in samples:
            self.add_sample(sample)

    def iter_items(self) -> Iterable[tuple[Interest, Sample]]:
        for interest, samples in self._interest_samples_map.items():
            for sample in samples:
                yield interest, sample

    def iter_interests(self) -> Iterable[Interest]:
        return self._interest_samples_map.keys()

    def iter_samples(self) -> Iterable[Sample]:
        for samples in self._interest_samples_map.values():
            yield from samples

    def langs(self) -> set[str]:
        return {interest.lang for interest in self.iter_interests()}
