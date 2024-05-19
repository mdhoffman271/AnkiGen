

import os
import time

from ankigen.src.format.anki import save_samples_as_anki
from ankigen.src.format.wiktionary import get_token_from_url, is_wiktionary_url
from ankigen.src.study.interest_store import InterestStore
from ankigen.src.study.source.epub import iter_samples_from_epub_folder
from ankigen.src.study.source.firefox import iter_firefox_wiktionary_urls
from ankigen.src.study.source.kaikki import iter_samples_from_kaikki
from ankigen.src.study.source.text import iter_samples_from_text_folder

for lang in ['de', 'es', 'fr']:
    print(f'Loading {lang}...')
    store = InterestStore(lang)
    start_time = time.time() - 61 * 24 * 60 * 60  # 2 months in the past

    for url in filter(is_wiktionary_url, iter_firefox_wiktionary_urls('./data/firefox/places.sqlite', min_epoch=start_time)):
        text = get_token_from_url(url)
        store.add_interest(text)

    store.add_samples(iter_samples_from_epub_folder('./data/epub', lang))
    store.add_samples(iter_samples_from_text_folder('./data/text', lang))
    store.add_samples(iter_samples_from_kaikki('./data/kaikki/raw-wiktextract-data.json.gz', lang))

    path = f'./data/out/{lang}.txt'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    save_samples_as_anki(path, store.iter_samples())
