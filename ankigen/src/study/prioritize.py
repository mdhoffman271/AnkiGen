from typing import Iterable, Optional

from ankigen.src.study.interest import Interest
from ankigen.src.study.lemmatization import LemmaCollection, Lemmatization
from ankigen.src.study.sample import Sample


def prioritize(samples: Iterable[Sample], interests: Iterable[Interest], samples_per_interest=3) -> Iterable[Sample]:
    cache: dict[Interest, list[Sample]] = {i: list() for i in interests if len(i.lemmas) > 0}

    # Map each interest to some samples.
    for sample in samples:
        sample_lemma_set = set(sample.lemmatization.lemmas)
        for interest in cache.keys():
            if _is_match(sample_lemma_set, interest.lemmas):
                cache[interest] = list(_discard_extras(cache[interest] + [sample], samples_per_interest))

    # Remove duplicate samples.
    unique_samples = set()
    unique_samples.update(*cache.values())

    return sorted(unique_samples, key=lambda s: s.effort)


def _discard_extras(samples: Iterable[Sample], max_count) -> Iterable[Sample]:
    # Remove duplicates.
    cache: dict[Lemmatization, Sample] = dict()
    for sample in samples:
        key = sample.lemmatization
        other = cache.get(key, None)
        cache[key] = _better_sample(sample, other)

    # Shorten to max_samples.
    return sorted(cache.values(), key=lambda x: x.effort)[:max_count]


def _is_match(sample_lemma_set: set[str], interest_lemmas: LemmaCollection) -> bool:
    for lemma in interest_lemmas:
        if lemma not in sample_lemma_set:
            return False
    return True


def _better_sample(sample: Sample, other: Optional[Sample]) -> Sample:
    if other is None:
        return sample
    sample_score = _data_score(sample)
    other_score = _data_score(other)

    # Return the best sample, using len(text) as a tie-breaker.
    if sample_score > other_score:
        return sample
    elif sample_score == other_score and len(sample.text) < len(other.text):
        return sample
    else:
        return other


def _data_score(sample: Sample) -> int:
    score = 0
    if sample.source is not None:
        score += 2
    if sample.english is not None:
        score += 1
    return score
