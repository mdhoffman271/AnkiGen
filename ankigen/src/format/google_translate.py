from urllib.parse import quote


def get_translation_url(text: str, source_lang: str, target_lang: str = 'en') -> str:
    return f'https://translate.google.com/?sl={source_lang}&tl={target_lang}&text={quote(text)}&op=translate'
