

import os
from glob import iglob
from typing import Iterable

from ankigen.src.study.sample import Sample
from ankigen.src.transform.sentence import iter_sentences
from ankigen.src.transform.text import clean


def iter_samples_from_text(path: str, lang: str) -> Iterable[Sample]:
    with open(path, 'r', encoding='utf8') as file:
        text = file.read()
        for sentence in iter_sentences(text, lang):
            yield Sample(lang, clean(sentence))


def iter_samples_from_text_folder(root_path: str, lang: str) -> Iterable[Sample]:
    for text_path in iglob(os.path.join(root_path, lang, '**', '*.txt'), recursive=True):
        yield from iter_samples_from_text(text_path, lang)
