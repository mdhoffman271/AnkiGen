import gzip
import json
from typing import Iterable

from ankigen.src.data.text import clean
from ankigen.src.data.wiktionary import get_url_from_text
from ankigen.src.study.context import ActiveContext
from ankigen.src.study.sample import Sample


def iter_samples_from_kaikki(context: ActiveContext, path: str) -> Iterable[Sample]:
    needle = f'"lang_code": "{context.lang}"'
    with gzip.open(path, 'rt', encoding='utf8') as file:
        for line in file:
            if needle in line:
                data = json.loads(line)
                lang = data.get('lang_code', None)
                if lang != context.lang:
                    continue
                word = data.get('word', None)
                if word is None:
                    continue
                url = get_url_from_text(word, lang)
                yield Sample(context, clean(word), url)
                for sense in data.get('senses', []):
                    for example in sense.get('examples', []):
                        text = example.get('text', None)
                        if text is not None:
                            text = clean(text)
                            english = example.get('english', None)
                            if english is not None:
                                english = clean(english)
                            yield Sample(context, text, url, english)
