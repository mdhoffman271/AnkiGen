from typing import Iterable

from ankigen.src.study.interest import Interest
from ankigen.src.study.lemmatization import LemmaCollection, Lemmatization
from ankigen.src.study.sample import Sample


class Store:
    def __init__(self, max_samples=3) -> None:
        self.max_samples = max_samples

    def filter(self, samples: Iterable[Sample], interests: Iterable[Interest]) -> set[Sample]:
        cache: dict[Interest, list[Sample]] = {i: list() for i in interests if len(i.lemmas) > 0}

        # Map each interest to some samples.
        for sample in samples:
            sample_lemma_set = set(sample.lemmatization.lemmas)
            for interest in cache.keys():
                if _is_match(sample_lemma_set, interest.lemmas):
                    cache[interest] = list(self._discard_extras(cache[interest] + [sample]))

        # Remove duplicate samples.
        result = set()
        result.update(*cache.values())
        return result

    def _discard_extras(self, samples: Iterable[Sample]) -> Iterable[Sample]:
        # Remove duplicates.
        cache: dict[Lemmatization, Sample] = dict()
        for sample in samples:
            key = sample.lemmatization
            other = cache.get(key, None)
            if (other is None
                    or sample.source is not None and other.source is None
                    or sample.english is not None and other.english is None
                    or len(sample.text) < len(other.text)
                ):
                cache[key] = sample
            else:
                cache[key] = other

        # Shorten to max_samples.
        return sorted(cache.values(), key=lambda x: x.effort)[:self.max_samples]


def _is_match(sample_lemma_set: set[str], interest_lemmas: LemmaCollection) -> bool:
    for lemma in interest_lemmas:
        if lemma not in sample_lemma_set:
            return False
    return True
