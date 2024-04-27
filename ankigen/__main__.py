

import time
from itertools import islice

from ankigen.src.epub import iter_samples_in_root
from ankigen.src.firefox import iter_firefox_wiktionary_urls
from ankigen.src.sentence import is_valid_word, iter_words
from ankigen.src.wiktionary import get_word_from_url, is_wiktionary_url

thingies = dict()
start_time = time.time() - 61 * 24 * 60 * 60

for url in filter(is_wiktionary_url, iter_firefox_wiktionary_urls('./data/firefox/places.sqlite', min_epoch=start_time)):
    text = get_word_from_url(url)
    key = tuple(sorted(filter(lambda x: is_valid_word(x, 'es'), iter_words(text, 'es'))))
    if len(key) > 0:
        thingies[key] = set()

for sample in iter_samples_in_root('./data/epub', 'es'):
    for lemmas, samples in thingies.items():
        for lemma in lemmas:
            if lemma not in sample.unique_tokens:
                break
        else:
            samples.add(sample)

for key, value in thingies.items():
    print(key)
    print(list(islice(sorted(value, key=lambda x: x.effort), 3)))
