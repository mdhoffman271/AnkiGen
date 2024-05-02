
from typing import Iterable

from ankigen.src.sample import Sample


def escape_str(text: str) -> str:
    return f'"{text.replace('"', '""')}"'


def save_dict_as_anki(path: str, data: dict[str, str]) -> None:
    with open(path, 'w', encoding='utf8') as file:
        for key, value in data.items():
            file.write(f'{escape_str(key)};{escape_str(value)}\n')


def save_samples_as_anki(path: str, samples: Iterable[Sample]) -> None:
    with open(path, 'w', encoding='utf8') as file:
        for sample in samples:
            front = sample.text
            back = '' if sample.url is None else f'<a href="{sample.url}">Source</a>'
            file.write(f'{escape_str(front)};{escape_str(back)}\n')
