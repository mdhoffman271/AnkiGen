import sqlite3
from typing import Iterable

from ankigen.src.data.wiktionary import get_text_from_url, is_wiktionary_url
from ankigen.src.study.context import ActiveContext
from ankigen.src.study.interest import Interest


def iter_urls_from_firefox_wiktionary(path: str, start_time=float('-inf'), end_time=float('inf')) -> Iterable[str]:
    conn = sqlite3.connect(path)
    query = r"SELECT url FROM moz_places WHERE url LIKE '%wiktionary.org/wiki/%'"
    if start_time > float('-inf'):
        query += rf" AND last_visit_date >= {int(start_time * 1e6)}"
    if end_time < float('inf'):
        query += rf" AND last_visit_date <= {int(end_time * 1e6)}"
    for result in conn.execute(query).fetchall():
        url = result[0]
        if is_wiktionary_url(url):
            yield url
    conn.close()


def iter_interests_from_firefox_wiktionary(context: ActiveContext, path: str, start_time=float('-inf'), end_time=float('inf')) -> Iterable[Interest]:
    for url in iter_urls_from_firefox_wiktionary(path, start_time, end_time):
        yield Interest.from_text(context, get_text_from_url(url))
