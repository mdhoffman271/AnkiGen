import re
from typing import Optional
from urllib.parse import quote, unquote, urlparse

_URL_PATTERN = re.compile(r'https://en(?:\.m)?\.wiktionary.org/wiki/.*')


def is_wiktionary_url(url: str) -> bool:
    return bool(_URL_PATTERN.fullmatch(url))


def get_text_from_url(url: str) -> str:
    result = urlparse(url)
    if result.netloc not in ('en.wiktionary.org', 'en.m.wiktionary.org'):
        raise Exception(f'Invalid netloc: {result.netloc}')
    if not result.path.startswith('/wiki/'):
        raise Exception(f'Invalid path: {result.path}')
    return unquote(result.path[6:]).replace('_', ' ')


def get_url_from_text(text: str, lang: Optional[str] = None) -> str:
    url = f'https://en.wiktionary.org/wiki/{quote(text.replace(' ', '_'))}'
    if lang is not None:
        language = _LANG_LANGUAGE_MAP.get(lang, None)
        if language is not None:
            url += f'#{quote(language)}'
    return url


# TODO add more here.
_LANG_LANGUAGE_MAP = {
    'de': 'German',
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
}
