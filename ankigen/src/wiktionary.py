import re
from typing import Optional
from urllib.parse import quote, unquote, urlparse

WIKTIONARY_URL_PATTERN = re.compile(r'https://en(?:\.m)?\.wiktionary.org/wiki/.*')


def is_wiktionary_url(url: str) -> bool:
    return bool(WIKTIONARY_URL_PATTERN.fullmatch(url))


def get_token_from_url(url: str) -> str:
    result = urlparse(url)
    if result.netloc not in ('en.wiktionary.org', 'en.m.wiktionary.org'):
        raise Exception(f'Invalid netloc: {result.netloc}')
    if not result.path.startswith('/wiki/'):
        raise Exception(f'Invalid path: {result.path}')
    return unquote(result.path[6:]).replace('_', ' ')


def get_url_from_token(token: str, language: Optional[str] = None) -> str:
    url = f'https://en.wiktionary.org/wiki/{quote(token.replace(' ', '_'))}'
    if language is not None:
        url += f'#{quote(language)}'
    return url
