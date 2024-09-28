import time
from dataclasses import dataclass
from glob import iglob
from typing import Callable, Iterable, Optional, Self

from ankigen.src.data.anki import save_samples_as_anki
from ankigen.src.study.context import ActiveContext
from ankigen.src.study.interest import Interest
from ankigen.src.study.prioritize import prioritize
from ankigen.src.study.sample import Sample
from ankigen.src.study.sources.epub import iter_samples_from_epub
from ankigen.src.study.sources.firefox import iter_interests_from_firefox_wiktionary
from ankigen.src.study.sources.kaikki import iter_samples_from_kaikki
from ankigen.src.study.sources.text import iter_samples_from_text


@dataclass()
class AnkiResult:
    lang: str
    interests: set[Interest]
    sample_to_interests_map: dict[Sample, set[Interest]]

    def samples(self) -> Iterable[Sample]:
        return self.sample_to_interests_map.keys()

    def satisfied_interests(self) -> set[Interest]:
        return {interest for interests in self.sample_to_interests_map.values() for interest in interests}

    def unsatisfied_interests(self) -> set[Interest]:
        return self.interests.difference(self.satisfied_interests())

    def save(self, path: str) -> None:
        save_samples_as_anki(path, sorted(self.samples(), key=lambda s: s.effort), self.lang)


class AnkiBuilder:
    def __init__(self, context: ActiveContext, log_func: Optional[Callable[[str], None]] = print) -> None:
        if log_func is None:
            log_func = _no_log

        self._context = context
        self._log_func = log_func
        self._interest_generators: list[Callable[[], Iterable[Interest]]] = []
        self._sample_generators: list[Callable[[], Iterable[Sample]]] = []

    def build(self) -> AnkiResult:
        self._log_func(f"starting build (lang: '{self._context.lang}') ...")
        interests = set(i for i in self._iter_interests() if len(i.lemmas) > 0)
        sample_to_interests_map = prioritize(self._iter_samples(), interests)
        self._log_func(f'finished build')
        return AnkiResult(self._context.lang, interests, sample_to_interests_map)

    def with_firefox_wiktionary(self, path: str, past_day_count: float) -> Self:
        def func() -> Iterable[Interest]:
            self._log_func(f"loading interests (firefox_wiktionary) from '{path}' ...")
            return iter_interests_from_firefox_wiktionary(self._context, path, time.time() - past_day_count * 24 * 60 * 60)
        self._interest_generators.append(func)
        return self

    def with_epub(self, glob: str) -> Self:
        def func() -> Iterable[Sample]:
            for path in _iter_paths(glob):
                self._log_func(f"loading samples (epub) from '{path}' ...")
                yield from iter_samples_from_epub(self._context, path)
        self._sample_generators.append(func)
        return self

    def with_text(self, glob: str) -> Self:
        def func() -> Iterable[Sample]:
            for path in _iter_paths(glob):
                self._log_func(f"loading samples (text) from '{path}' ...")
                yield from iter_samples_from_text(self._context, path)
        self._sample_generators.append(func)
        return self

    def with_kaikki(self, path: str) -> Self:
        def func() -> Iterable[Sample]:
            self._log_func(f"loading samples (kaikki) from '{path}' ...")
            yield from iter_samples_from_kaikki(self._context, path)
        self._sample_generators.append(func)
        return self

    def _iter_interests(self) -> Iterable[Interest]:
        for interest_generator in self._interest_generators:
            yield from interest_generator()

    def _iter_samples(self) -> Iterable[Sample]:
        for sample_generator in self._sample_generators:
            yield from sample_generator()


def _iter_paths(glob: str) -> Iterable[str]:
    return iglob(glob, recursive=True)


def _no_log(_: str) -> None:
    return None
