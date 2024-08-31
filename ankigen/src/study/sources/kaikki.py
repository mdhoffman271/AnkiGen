

import gzip
import json
from typing import Iterable

from ankigen.src.format.wiktionary import get_language_from_lang, get_url_from_token
from ankigen.src.language.text import clean
from ankigen.src.study.sample import Sample


def iter_samples_from_kaikki(path: str, langs: Iterable[str]) -> Iterable[Sample]:
    lang_language_map = {lang: get_language_from_lang(lang) for lang in langs}
    needles = {f'"lang_code": "{lang}"' for lang in lang_language_map.keys()}
    with gzip.open(path, 'rt', encoding='utf8') as file:
        for line in file:
            if text_contains_some(line, needles):
                data = json.loads(line)
                lang = data['lang_code']
                language = lang_language_map.get(lang, None)
                if language is None:
                    continue
                word = data.get('word', None)
                if word is None:
                    continue
                url = get_url_from_token(word, language)
                yield Sample(lang, clean(word), url)
                for sense in data.get('senses', []):
                    for example in sense.get('examples', []):
                        text = example.get('text', None)
                        translation = example.get('english', None)
                        if text is not None:
                            yield Sample(lang, clean(text), url, translation)


def text_contains_some(text: str, needles: set[str]) -> bool:
    for needle in needles:
        if needle in text:
            return True
    return False
