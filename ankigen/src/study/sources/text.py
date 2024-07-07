
from typing import Iterable

from ankigen.src.language.sentence import iter_sentences
from ankigen.src.language.text import clean
from ankigen.src.study.sample import Sample


def iter_samples_from_text(path: str, lang: str) -> Iterable[Sample]:
    with open(path, 'r', encoding='utf8') as file:
        text = file.read()
        for sentence in iter_sentences(text, lang):
            yield Sample(lang, clean(sentence))
