

import os
from glob import iglob
from typing import Iterable

from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub

from ankigen.src.sample import Sample
from ankigen.src.sentence import iter_sentences


def iter_samples_from_epub(path: str, lang: str) -> Iterable[Sample]:
    book = epub.read_epub(path)

    for doc in book.get_items_of_type(ITEM_DOCUMENT):
        html = doc.get_content()
        soup = BeautifulSoup(html, 'html.parser')
        for paragraph in soup.find_all('p'):
            for sentence in iter_sentences(paragraph.get_text(), lang):
                yield Sample(lang, sentence)


def iter_samples_in_root(root_path: str, lang: str) -> Iterable[Sample]:
    for epub_path in iglob(os.path.join(root_path, lang, '**', '*.epub'), recursive=True):
        yield from iter_samples_from_epub(epub_path, lang)
