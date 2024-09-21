import time
from glob import iglob
from typing import Callable, Iterable, Optional, Self

from ankigen.src.data.anki import save_samples_as_anki
from ankigen.src.study.context import ActiveContext
from ankigen.src.study.interest import Interest
from ankigen.src.study.sample import Sample
from ankigen.src.study.sources.epub import iter_samples_from_epub
from ankigen.src.study.sources.firefox import iter_firefox_wiktionary_interests
from ankigen.src.study.sources.kaikki import iter_samples_from_kaikki
from ankigen.src.study.sources.text import iter_samples_from_text
from ankigen.src.study.store import Store


class AnkiBuilder:

    def __init__(self, lang: str, log_func: Optional[Callable[[str], None]] = print) -> None:
        if log_func is None:
            log_func = _no_log

        self._lang = lang
        self._log_func = log_func
        self._interest_generators: list[Callable[[], Iterable[Interest]]] = []
        self._sample_generators: list[Callable[[], Iterable[Sample]]] = []

    def generate(self, path: str) -> None:
        if path.endswith('/') or path.endswith('\\'):
            path += f'{self._lang}.txt'
        ActiveContext.lang = self._lang  # todo add lock or something
        store = Store()
        self._log_func(f"starting generate (lang: '{self._lang}') ...")
        samples = store.filter(self._iter_samples(), self._iter_interests())
        self._log_func(f"saving samples to {path} ...")
        save_samples_as_anki(path, samples, self._lang)
        self._log_func("done")

    def with_firefox_wiktionary(self, path: str, past_day_count: float) -> Self:
        def func() -> Iterable[Interest]:
            self._log_func(f"loading interests (firefox_wiktionary) from '{path}' ...")
            return iter_firefox_wiktionary_interests(path, time.time() - past_day_count * 24 * 60 * 60)
        self._interest_generators.append(func)
        return self

    def with_epub(self, glob: str) -> Self:
        def func() -> Iterable[Sample]:
            for path in _iter_paths(glob):
                self._log_func(f"loading samples (epub) from '{path}' ...")
                yield from iter_samples_from_epub(path)
        self._sample_generators.append(func)
        return self

    def with_text(self, glob: str) -> Self:
        def func() -> Iterable[Sample]:
            for path in _iter_paths(glob):
                self._log_func(f"loading samples (text) from '{path}' ...")
                yield from iter_samples_from_text(path)
        self._sample_generators.append(func)
        return self

    def with_kaikki(self, path: str) -> Self:
        def func() -> Iterable[Sample]:
            self._log_func(f"laoding samples (kaikki) from '{path}' ...")
            yield from iter_samples_from_kaikki(path)
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