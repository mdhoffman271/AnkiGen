
import itertools
import os
import sys
import time
from typing import Iterable, Optional

from ankigen.src.format.anki import save_samples_as_anki
from ankigen.src.format.wiktionary import get_token_from_url
from ankigen.src.study.interest_store import InterestStore
from ankigen.src.study.sample import Sample
from ankigen.src.study.sources.epub import iter_samples_from_epub_folder
from ankigen.src.study.sources.firefox import iter_firefox_wiktionary_urls
from ankigen.src.study.sources.kaikki import iter_samples_from_kaikki
from ankigen.src.study.sources.text import iter_samples_from_text_folder

# argparse wasn't doing what I wanted, so I wrote some custom stuff here.
# Example:
# python -m ankigen es --epub ./data/epub --text ./data/text --kaikki ./data/kaikki/raw-wiktextract-data.jsonl.gz

Args = list[str]


def exit_with_reason(text: str) -> None:
    print(text)
    exit(0)  # todo this should probably not be 0


class LazyLoader:
    def __init__(self, lang: str, interests: Optional[Iterable[str]] = None, samples: Optional[Iterable[Sample]] = None) -> None:
        if interests is None:
            interests = []
        if samples is None:
            samples = []
        self.interests = interests
        self.samples = samples
        self.lang = lang

    def add_interests(self, interests: Iterable[str]) -> None:
        self.interests = itertools.chain(self.interests, interests)

    def add_samples(self, samples: Iterable[Sample]) -> None:
        self.samples = itertools.chain(self.samples, samples)


def parse_all(args: Args) -> None:
    lang = args[0]

    loader = LazyLoader(lang)
    parse_remainder(loader, args[1:])

    store = InterestStore(lang)

    # todo should probably rewrite this somehow to guarantee add_interests before add_samples
    store.add_interests(loader.interests)

    # todo make param
    start_time = time.time() - 61 * 24 * 60 * 60  # 2 months in the past

    # todo make param
    for url in iter_firefox_wiktionary_urls('./data/firefox/places.sqlite', min_epoch=start_time):
        text = get_token_from_url(url)
        store.add_interest(text)

    store.add_samples(loader.samples)

    # todo make param
    path = f'./data/out/{lang}.txt'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    save_samples_as_anki(path, store.iter_samples())


def parse_remainder(loader: LazyLoader, args: Args) -> LazyLoader:
    if len(args) == 0:
        return loader
    func_map = {
        '--epub': parse_epub,
        '--text': parse_text,
        '--kaikki': parse_kaikki
    }
    name, args = args[0], args[1:]
    parse_func = func_map.get(name, None)
    if parse_func is None:
        exit_with_reason(f'Unexpected arg: {name}')
        return loader
    return parse_func(loader, args)


def parse_epub(loader: LazyLoader, args: Args) -> LazyLoader:
    path, args = args[0], args[1:]

    print(f'Using epub samples from path: {path}.')
    loader.add_samples(iter_samples_from_epub_folder(path, loader.lang))

    return parse_remainder(loader, args)


def parse_text(loader: LazyLoader, args: Args) -> LazyLoader:
    path, args = args[0], args[1:]

    print(f'Using text samples from path: {path}.')
    loader.add_samples(iter_samples_from_text_folder(path, loader.lang))

    return parse_remainder(loader, args)


def parse_kaikki(loader: LazyLoader, args: Args) -> LazyLoader:
    path, args = args[0], args[1:]

    print(f'Using Kaikki samples from path: {path}.')
    loader.add_samples(iter_samples_from_kaikki(path, loader.lang))

    return parse_remainder(loader, args)


parse_all(sys.argv[1:])
