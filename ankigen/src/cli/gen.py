

from abc import ABC, abstractmethod
from dataclasses import dataclass
from glob import iglob
import json
import os
import time
from typing import Any, Iterable, Optional

from ankigen.src.format.anki import save_samples_as_anki
from ankigen.src.study.interest_store import InterestStore
from ankigen.src.study.sources.epub import iter_samples_from_epub
from ankigen.src.study.sources.firefox import iter_firefox_wiktionary_interests
from ankigen.src.study.sources.kaikki import iter_samples_from_kaikki
from ankigen.src.study.sources.text import iter_samples_from_text


def generate_anki(lang: str, spec_path: str, out_path: str) -> None:
    spec = load_spec(spec_path)

    interest_actions: list[InterestAction] = []
    sample_actions: list[SampleAction] = []

    for glob, options in spec.items():
        interest_actions += iter_interests(glob, options)
        sample_actions += iter_samples(glob, lang, options)

    store = InterestStore(lang)

    # todo should probably rewrite this to guarantee add_interests before add_samples
    print('Loading interests ...')
    for action in interest_actions:
        action.execute(store)

    print('Loading samples ...')
    for action in sample_actions:
        action.execute(store)

    print(f'Writing to file {out_path}')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    save_samples_as_anki(out_path, store.iter_samples())


JsonLike = Any


def load_spec(spec_path: str) -> JsonLike:
    if spec_path.endswith('.json'):
        with open(spec_path, 'r') as file:
            return json.load(file)
    elif spec_path.endswith('.yaml'):
        raise NotImplementedError()
    else:
        raise Exception()  # todo


class InterestAction(ABC):
    @abstractmethod
    def execute(self, interest_store: InterestStore) -> None:
        raise NotImplementedError()


@dataclass(frozen=True)
class WiktionaryOptions:
    last_days_range: Optional[float]

    @staticmethod
    def range_to_seconds(range: float) -> float:
        return time.time() - range * 24 * 60 * 60

    def get_start_time(self) -> float:
        if self.last_days_range is None:
            return float('-inf')
        return self.range_to_seconds(self.last_days_range)

    @staticmethod
    def from_options(options: JsonLike) -> Optional['WiktionaryOptions']:
        if wiktionary := options.get('wiktionary', None):
            last_days_range = wiktionary.get('last_days_range', None)
            return WiktionaryOptions(last_days_range)


class FirefoxAction(InterestAction):
    def __init__(self, glob: str, wiktionary: Optional[WiktionaryOptions]) -> None:
        super().__init__()
        self.glob = glob
        self.wiktionary = wiktionary

    def execute(self, interest_store: InterestStore) -> None:
        for path in iter_glob_paths(self.glob):
            if self.wiktionary is not None:
                print(f'Loading Wiktionary data from {path} ...')
                start_time = self.wiktionary.get_start_time()
                interest_store.add_interests(iter_firefox_wiktionary_interests(path, start_time))

    @staticmethod
    def from_options(glob: str, options: JsonLike) -> Optional['FirefoxAction']:
        if firefox := options.get('firefox', None):
            wiktionary = WiktionaryOptions.from_options(firefox)
            return FirefoxAction(glob, wiktionary)


class SampleAction(ABC):
    @abstractmethod
    def execute(self, interest_store: InterestStore) -> None:
        raise NotImplementedError()


class EpubAction(SampleAction):
    def __init__(self, glob: str, lang: str) -> None:
        super().__init__()
        self.glob = glob
        self.lang = lang

    def execute(self, interest_store: InterestStore) -> None:
        for path in iter_glob_paths(self.glob):
            print(f'Loading epub data from {path} ...')
            interest_store.add_samples(iter_samples_from_epub(path, self.lang))

    @staticmethod
    def from_options(glob: str, lang: str, options: JsonLike) -> Optional['EpubAction']:
        if 'epub' in options:
            return EpubAction(glob, lang)


class KaikkiAction(SampleAction):
    def __init__(self, glob: str, lang: str) -> None:
        super().__init__()
        self.glob = glob
        self.lang = lang

    def execute(self, interest_store: InterestStore) -> None:
        for path in iter_glob_paths(self.glob):
            print(f'Loading Kaikki data from {path} ...')
            interest_store.add_samples(iter_samples_from_kaikki(path, self.lang))

    @staticmethod
    def from_options(glob: str, lang: str, options: JsonLike) -> Optional['KaikkiAction']:
        if 'kaikki' in options:
            return KaikkiAction(glob, lang)


class TextAction(SampleAction):
    def __init__(self, glob: str, lang: str) -> None:
        super().__init__()
        self.glob = glob
        self.lang = lang

    def execute(self, interest_store: InterestStore) -> None:
        for path in iter_glob_paths(self.glob):
            print(f'Loading text data from {path} ...')
            interest_store.add_samples(iter_samples_from_text(path, self.lang))

    @staticmethod
    def from_options(glob: str, lang: str, options: JsonLike) -> Optional['TextAction']:
        if 'text' in options:
            return TextAction(glob, lang)


def iter_glob_paths(text: str) -> Iterable[str]:
    return iglob(text, recursive=True)


def iter_interests(glob: str, options: JsonLike) -> Iterable[InterestAction]:
    for action in [FirefoxAction.from_options(glob, options)]:
        if action is not None:
            yield action


def iter_samples(glob: str, lang: str, options: JsonLike) -> Iterable[SampleAction]:
    for action in [
        EpubAction.from_options(glob, lang, options),
        KaikkiAction.from_options(glob, lang, options),
        TextAction.from_options(glob, lang, options),
    ]:
        if action is not None:
            yield action
