
import os
import sys
import time

from ankigen.src.format.anki import save_samples_as_anki
from ankigen.src.format.wiktionary import get_token_from_url
from ankigen.src.study.interest_store import InterestStore
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


def parse_all(args: Args) -> None:
    lang = args[0]
    store = InterestStore(lang)

    # todo make param
    start_time = time.time() - 61 * 24 * 60 * 60  # 2 months in the past

    # todo make param
    for url in iter_firefox_wiktionary_urls('./data/firefox/places.sqlite', min_epoch=start_time):
        text = get_token_from_url(url)
        store.add_interest(text)

    # todo need to make this happen after adding interests
    parse_remainder(store, args[1:])

    # todo make param
    path = f'./data/out/{lang}.txt'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    save_samples_as_anki(path, store.iter_samples())


def parse_remainder(store: InterestStore, args: Args) -> None:
    print(args)  # todo remove
    if len(args) == 0:
        return
    func_map = {
        '--epub': parse_epub,
        '--text': parse_text,
        '--kaikki': parse_kaikki
    }
    arg, remainder = args[0], args[1:]
    parse_func = func_map.get(arg, None)
    if parse_func is None:
        exit_with_reason(f'Unexpected arg: {arg}')
        return
    parse_func(store, remainder)


def parse_epub(store: InterestStore, args: Args) -> None:
    path, remainder = args[0], args[1:]
    parse_remainder(store, remainder)

    print(f'Loading epub samples from path: {path} ...')
    store.add_samples(iter_samples_from_epub_folder(path, store.lang))


def parse_text(store: InterestStore, args: Args) -> None:
    path, remainder = args[0], args[1:]
    parse_remainder(store, remainder)

    print(f'Loading text samples from path: {path} ...')
    store.add_samples(iter_samples_from_text_folder(path, store.lang))


def parse_kaikki(store: InterestStore, args: Args) -> None:
    path, remainder = args[0], args[1:]
    parse_remainder(store, remainder)

    print(f'Loading kaikki samples from path: {path} ...')
    store.add_samples(iter_samples_from_kaikki(path, store.lang))


parse_all(sys.argv[1:])
