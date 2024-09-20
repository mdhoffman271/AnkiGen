import time
from glob import iglob
from itertools import chain, islice
from typing import Iterable

from ankigen.src.data.anki import save_samples_as_anki
from ankigen.src.study.context import ActiveContext
from ankigen.src.study.sources.epub import iter_samples_from_epub
from ankigen.src.study.sources.firefox import iter_firefox_wiktionary_interests
from ankigen.src.study.sources.kaikki import iter_samples_from_kaikki
from ankigen.src.study.sources.text import iter_samples_from_text
from ankigen.src.study.store import Store


def main():
    for lang in ['de', 'es', 'fr']:
        load(lang)


def load(lang: str):
    ActiveContext.lang = lang
    sample_iterables = []

    for path in iter_paths(f'./data/epub/{lang}/**/*.epub'):
        sample_iterables.append(iter_samples_from_epub(path))

    for path in iter_paths(f'./data/kaikki/raw-wiktextract-data.jsonl.gz'):
        sample_iterables.append(iter_samples_from_kaikki(path))

    for path in iter_paths(f'./data/text/{lang}/**/*.txt'):
        sample_iterables.append(iter_samples_from_text(path))

    samples = chain(*sample_iterables)
    interests = iter_firefox_wiktionary_interests('./data/firefox/places.sqlite', time.time() - 61 * 24 * 60 * 60)

    store = Store()
    out_path = f'./data/out/{lang}.text'
    save_samples_as_anki(out_path, store.filter(samples, interests), lang)


def iter_paths(glob: str) -> Iterable[str]:
    return iglob(glob, recursive=True)


main()
