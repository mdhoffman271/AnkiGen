import os
from typing import Iterable

from ankigen.src.data.text import clean
from ankigen.src.study.context import ActiveContext
from ankigen.src.study.sample import Sample


def iter_samples_from_text(path: str) -> Iterable[Sample]:
    filename = os.path.basename(path)
    with open(path, 'r', encoding='utf8') as file:
        text = file.read()
        for sentence in ActiveContext.iter_sentences(text):
            yield Sample(clean(sentence), filename)
