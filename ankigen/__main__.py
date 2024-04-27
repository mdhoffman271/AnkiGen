

import time

from ankigen.src.epub import iter_samples_in_root
from ankigen.src.firefox import iter_firefox_wiktionary_urls
from ankigen.src.interest_store import InterestStore
from ankigen.src.wiktionary import get_token_from_url, is_wiktionary_url

store = InterestStore('es')
start_time = time.time() - 61 * 24 * 60 * 60

for url in filter(is_wiktionary_url, iter_firefox_wiktionary_urls('./data/firefox/places.sqlite', min_epoch=start_time)):
    text = get_token_from_url(url)
    store.add_interest(text)

store.add_samples(iter_samples_in_root('./data/epub', 'es'))

for key, value in store.iter_items():
    print(key)
    print(value)
