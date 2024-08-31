

from abc import ABC, abstractmethod
from dataclasses import dataclass
from glob import iglob
import json
import os
import time
from typing import Any, Iterable, Optional

from ankigen.src.format.anki import save_samples_as_anki
from ankigen.src.study.interest import Interest
from ankigen.src.study.sample_store import SampleStore
from ankigen.src.study.sources.epub import iter_samples_from_epub
from ankigen.src.study.sources.firefox import iter_firefox_wiktionary_interests
from ankigen.src.study.sources.kaikki import iter_samples_from_kaikki
from ankigen.src.study.sources.text import iter_samples_from_text


def generate_anki(spec_path: str, out_dir: str) -> None:
    spec = load_spec(spec_path)

    interest_actions: list[InterestAction] = []
    sample_actions: list[SampleAction] = []

    for glob, options in spec.items():
        interest_actions += iter_interests(glob, options)
        sample_actions += iter_samples(glob, options)

    interest_store = set()

    print('Loading interests ...')
    for action in interest_actions:
        action.execute(interest_store)

    sample_store = SampleStore(3, interest_store)

    print('Loading samples ...')
    for action in sample_actions:
        action.execute(sample_store)

    print('Writing output ...')
    os.makedirs(os.path.dirname(out_dir), exist_ok=True)
    for lang in sample_store.langs():
        file_name = f'{lang}.txt'
        out_path = os.path.join(out_dir, file_name)
        print(f'Writing to {file_name} ...')
        save_samples_as_anki(out_path, sample_store.iter_samples())


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
    def execute(self, interest_store: set[Interest]) -> None:
        raise NotImplementedError()


@dataclass(frozen=True)
class WiktionaryOptions:
    langs: set[str]
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
            langs = set(wiktionary.get('langs', []))
            return WiktionaryOptions(langs, last_days_range)


class FirefoxAction(InterestAction):
    def __init__(self, glob: str, wiktionary: Optional[WiktionaryOptions]) -> None:
        super().__init__()
        self.glob = glob
        self.wiktionary = wiktionary

    def execute(self, interest_store: set[Interest]) -> None:
        for path in iter_glob_paths(self.glob):
            if self.wiktionary is not None:
                print(f'Loading Wiktionary data from {path} ...')
                start_time = self.wiktionary.get_start_time()
                interest_store.update(iter_firefox_wiktionary_interests(path, self.wiktionary.langs, start_time))

    @staticmethod
    def from_options(glob: str, options: JsonLike) -> Optional['FirefoxAction']:
        if firefox := options.get('firefox', None):
            wiktionary = WiktionaryOptions.from_options(firefox)
            return FirefoxAction(glob, wiktionary)


class SampleAction(ABC):
    @abstractmethod
    def execute(self, sample_store: SampleStore) -> None:
        raise NotImplementedError()


class EpubAction(SampleAction):
    def __init__(self, glob: str, lang: str) -> None:
        super().__init__()
        self.glob = glob
        self.lang = lang

    def execute(self, sample_store: SampleStore) -> None:
        for path in iter_glob_paths(self.glob):
            print(f'Loading epub data from {path} ...')
            sample_store.add_samples(iter_samples_from_epub(path, self.lang))

    @staticmethod
    def from_options(glob: str, options: JsonLike) -> Optional['EpubAction']:
        lang = options.get('epub', None)
        if lang is not None:
            return EpubAction(glob, lang)


class KaikkiAction(SampleAction):
    def __init__(self, glob: str, langs: Iterable[str]) -> None:
        super().__init__()
        self.glob = glob
        self.langs = set(langs)

    def execute(self, sample_store: SampleStore) -> None:
        for path in iter_glob_paths(self.glob):
            print(f'Loading Kaikki data from {path} ...')
            sample_store.add_samples(iter_samples_from_kaikki(path, self.langs))

    @staticmethod
    def from_options(glob: str, options: JsonLike) -> Optional['KaikkiAction']:
        langs = options.get('kaikki', None)
        if langs is not None:
            return KaikkiAction(glob, langs)


class TextAction(SampleAction):
    def __init__(self, glob: str, lang: str) -> None:
        super().__init__()
        self.glob = glob
        self.lang = lang

    def execute(self, sample_store: SampleStore) -> None:
        for path in iter_glob_paths(self.glob):
            print(f'Loading text data from {path} ...')
            sample_store.add_samples(iter_samples_from_text(path, self.lang))

    @staticmethod
    def from_options(glob: str, options: JsonLike) -> Optional['TextAction']:
        lang = options.get('text', None)
        if lang is not None:
            return TextAction(glob, lang)


def iter_glob_paths(text: str) -> Iterable[str]:
    return iglob(text, recursive=True)


def iter_interests(glob: str, options: JsonLike) -> Iterable[InterestAction]:
    for action in [FirefoxAction.from_options(glob, options)]:
        if action is not None:
            yield action


def iter_samples(glob: str, options: JsonLike) -> Iterable[SampleAction]:
    for action in [
        EpubAction.from_options(glob, options),
        KaikkiAction.from_options(glob, options),
        TextAction.from_options(glob, options),
    ]:
        if action is not None:
            yield action
