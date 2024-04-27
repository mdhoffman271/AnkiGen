

from typing import Optional

LANG_LANGUAGE_MAP = {
    'de': 'German',
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
}


def get_language_from_lang(lang: str) -> Optional[str]:
    return LANG_LANGUAGE_MAP.get(lang, None)
