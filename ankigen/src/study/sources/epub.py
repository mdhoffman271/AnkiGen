import os
from typing import Iterable

from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub

from ankigen.src.data.text import clean
from ankigen.src.study.context import ActiveContext
from ankigen.src.study.sample import Sample


def iter_samples_from_epub(context: ActiveContext, path: str) -> Iterable[Sample]:
    filename = os.path.basename(path)
    book = epub.read_epub(path, {"ignore_ncx": True})
    for doc in book.get_items_of_type(ITEM_DOCUMENT):
        html = doc.get_content()
        soup = BeautifulSoup(html, 'html.parser')
        for paragraph in soup.find_all('p'):
            for sentence in context.iter_sentences(paragraph.get_text()):
                yield Sample(context, clean(sentence), filename)
