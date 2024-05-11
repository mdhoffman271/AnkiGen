
from typing import Iterable

from ankigen.src.google_translate import get_translation_url
from ankigen.src.sample import Sample


def escape_str(text: str) -> str:
    return f'"{text.replace('"', '""')}"'


def save_samples_as_anki(path: str, samples: Iterable[Sample]) -> None:
    with open(path, 'w', encoding='utf8') as file:
        for sample in samples:
            front = sample.text
            back_parts = [f'<a href="{get_translation_url(sample.text, sample.lang)}">Translate</a>']
            if sample.url is not None:
                back_parts.append(f'<a href="{sample.url}">Source</a>')
            back = '<br>'.join(back_parts)
            file.write(f'{escape_str(front)};{escape_str(back)}\n')
