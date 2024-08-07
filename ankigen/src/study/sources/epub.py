
from typing import Iterable

from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub

from ankigen.src.language.sentence import iter_sentences
from ankigen.src.language.text import clean
from ankigen.src.study.sample import Sample


def iter_samples_from_epub(path: str, lang: str) -> Iterable[Sample]:
    book = epub.read_epub(path, {"ignore_ncx": True})
    for doc in book.get_items_of_type(ITEM_DOCUMENT):
        html = doc.get_content()
        soup = BeautifulSoup(html, 'html.parser')
        for paragraph in soup.find_all('p'):
            for sentence in iter_sentences(paragraph.get_text(), lang):
                yield Sample(lang, clean(sentence))
