import re

SPACE_PATTERN = re.compile(r'\s+')


def clean(text: str) -> str:
    text = SPACE_PATTERN.sub(' ', text)
    text = text.strip()
    return text
