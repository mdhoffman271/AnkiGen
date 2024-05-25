

import sqlite3
from typing import Iterable

from ankigen.src.format.wiktionary import is_wiktionary_url


def iter_firefox_wiktionary_urls(path: str, min_epoch=float('-inf'), max_epoch=float('inf')) -> Iterable[str]:
    conn = sqlite3.connect(path)
    query = r"SELECT url FROM moz_places WHERE url LIKE '%wiktionary.org/wiki/%'"
    if min_epoch > float('-inf'):
        query += rf" AND last_visit_date >= {int(min_epoch * 1e6)}"
    if max_epoch < float('inf'):
        query += rf" AND last_visit_date <= {int(max_epoch * 1e6)}"
    for result in conn.execute(query).fetchall():
        url = result[0]
        if is_wiktionary_url(url):
            yield url
    conn.close()
