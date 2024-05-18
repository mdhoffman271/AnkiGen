

import gzip
import json
from typing import Iterable

from ankigen.src.study.sample import Sample
from ankigen.src.text import clean
from ankigen.src.wiktionary import get_language_from_lang, get_url_from_token


def iter_samples_from_kaikki(path: str, lang: str) -> Iterable[Sample]:
    needle = f'"lang_code": "{lang}"'
    language = get_language_from_lang(lang)
    with gzip.open(path, 'rt', encoding='utf8') as file:
        for line in file:
            if needle not in line:
                continue
            data = json.loads(line)
            if data['lang_code'] != lang:
                continue
            word = data.get('word', None)
            if word is None:
                continue
            url = get_url_from_token(word, language)
            yield Sample(lang, clean(word), url)
            for sense in data.get('senses', []):
                for example in sense.get('examples', []):
                    text = example.get('text', None)
                    if text is not None:
                        yield Sample(lang, clean(text), url)
