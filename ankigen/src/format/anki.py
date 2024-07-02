
from typing import Iterable

from ankigen.src.format.google_translate import get_translation_url
from ankigen.src.study.sample import Sample


def escape_str(text: str) -> str:
    return f'"{text.replace('"', '""')}"'


def save_samples_as_anki(path: str, samples: Iterable[Sample]) -> None:
    with open(path, 'w', encoding='utf8') as file:
        for sample in samples:
            front = sample.text
            back_parts = [f'<a href="{get_translation_url(sample.text, sample.lang)}">Translate</a>']
            if sample.source_url is not None:
                back_parts.append(f'<a href="{sample.source_url}">Source</a>')
            if sample.translation is not None:
                back_parts.append(sample.translation)
            back = '<br><br>'.join(back_parts)
            file.write(f'{escape_str(front)};{escape_str(back)}\n')
