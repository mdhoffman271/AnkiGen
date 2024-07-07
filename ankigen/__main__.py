
import itertools
import os
import sys
import time
from glob import iglob
from typing import Iterable, Optional

from ankigen.src.format.anki import save_samples_as_anki
from ankigen.src.format.wiktionary import get_token_from_url
from ankigen.src.study.interest_store import InterestStore
from ankigen.src.study.sample import Sample
from ankigen.src.study.sources.epub import iter_samples_from_epub
from ankigen.src.study.sources.firefox import iter_firefox_wiktionary_interests
from ankigen.src.study.sources.kaikki import iter_samples_from_kaikki
from ankigen.src.study.sources.text import iter_samples_from_text

# argparse wasn't doing what I wanted, so I wrote some custom stuff here.
# Example:
# python -m ankigen es --epub "./data/epub/es/*.epub" --text "./data/text/es/*.txt" --kaikki "./data/kaikki/raw-wiktextract-data.jsonl.gz" --firefox "./data/firefox/places.sqlite" 61 0

Args = list[str]


def exit_with_reason(text: str) -> Exception:
    print(text)
    exit(0)  # todo this should probably not be 0


def iter_glob_paths(text: str) -> Iterable[str]:
    return iglob(text, recursive=True)


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


def print_help() -> None:
    print('todo')


def parse_all(args: Args) -> None:
    if len(args) == 0 or args[0] in ('-h', '--help'):
        print_help()
        return

    lang, args = get_first_arg(args)

    loader = LazyLoader(lang)
    parse_remainder(loader, args)

    store = InterestStore(lang)

    # todo should probably rewrite this somehow to guarantee add_interests before add_samples
    print('Loading interests...')
    store.add_interests(loader.interests)

    print('Loading samples...')
    store.add_samples(loader.samples)

    # todo make param
    path = f'./data/out/{lang}.txt'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    save_samples_as_anki(path, store.iter_samples())


def parse_remainder(loader: LazyLoader, args: Args) -> LazyLoader:
    if len(args) == 0:
        return loader
    func_map = {
        '--firefox': parse_firefox,
        '--epub': parse_epub,
        '--text': parse_text,
        '--kaikki': parse_kaikki,
    }
    name, args = args[0], args[1:]
    parse_func = func_map.get(name, None)
    if parse_func is None:
        raise exit_with_reason(f'Unexpected arg: {name}')
    return parse_func(loader, args)


def get_n_args(args: Args, count: int) -> tuple[list[str], Args]:
    if len(args) < count:
        err = f'Unexpected number of args. Expected {count} arg(s).\nStarting at:\n\t{''.join(args[:5])}'
        raise exit_with_reason(err)
    return args[:count], args[count:]


def get_first_arg(args: Args) -> tuple[str, Args]:
    first, args = get_n_args(args, 1)
    return first[0], args


def get_time_from_days(text: str) -> float:
    try:
        num = float(text)
    except ValueError:
        raise exit_with_reason(f'Could not convert value to number: {text}')
    return time.time() - num * 24 * 60 * 60


def parse_firefox(loader: LazyLoader, args: Args) -> LazyLoader:
    (glob, start, end), args = get_n_args(args, 3)
    start = get_time_from_days(start)
    end = get_time_from_days(end)
    parse_remainder(loader, args)

    for path in iter_glob_paths(glob):
        print(f'Using Firefox interests from path: {path}.')
        loader.add_interests(iter_firefox_wiktionary_interests(path, start, end))

    return loader


def parse_epub(loader: LazyLoader, args: Args) -> LazyLoader:
    glob, args = get_first_arg(args)
    loader = parse_remainder(loader, args)

    for path in iter_glob_paths(glob):
        print(f'Using epub samples from path: {path}.')
        loader.add_samples(iter_samples_from_epub(path, loader.lang))

    return loader


def parse_text(loader: LazyLoader, args: Args) -> LazyLoader:
    glob, args = get_first_arg(args)
    loader = parse_remainder(loader, args)

    for path in iter_glob_paths(glob):
        print(f'Using text samples from path: {path}.')
        loader.add_samples(iter_samples_from_text(path, loader.lang))

    return loader


def parse_kaikki(loader: LazyLoader, args: Args) -> LazyLoader:
    glob, args = get_first_arg(args)
    loader = parse_remainder(loader, args)

    for path in iter_glob_paths(glob):
        print(f'Using Kaikki samples from path: {path}.')
        loader.add_samples(iter_samples_from_kaikki(path, loader.lang))

    return loader


parse_all(sys.argv[1:])
