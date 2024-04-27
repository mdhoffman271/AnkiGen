

import sqlite3
from typing import Iterable


def iter_firefox_wiktionary_urls(path: str, min_epoch=float('-inf'), max_epoch=float('inf')) -> Iterable[str]:
    conn = sqlite3.connect(path)
    query = r"SELECT url FROM moz_places WHERE url LIKE '%wiktionary.org/wiki/%'"
    if min_epoch > float('-inf'):
        query += rf" AND last_visit_date >= {int(min_epoch * 1e6)}"
    if max_epoch < float('inf'):
        query += rf" AND last_visit_date <= {int(max_epoch * 1e6)}"
    for result in conn.execute(query).fetchall():
        yield result[0]
    conn.close()
