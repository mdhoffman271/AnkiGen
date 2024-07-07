

import sqlite3
from typing import Iterable

from ankigen.src.format.wiktionary import get_token_from_url, is_wiktionary_url


def iter_firefox_wiktionary_urls(path: str, start_time=float('-inf'), end_time=float('inf')) -> Iterable[str]:
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


def iter_firefox_wiktionary_interests(path: str, start_time=float('-inf'), end_time=float('inf')) -> Iterable[str]:
    for url in iter_firefox_wiktionary_urls(path, start_time, end_time):
        yield get_token_from_url(url)
