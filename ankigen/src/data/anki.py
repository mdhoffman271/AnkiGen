
from typing import Iterable

import validators

from ankigen.src.data.google_translate import get_translation_url
from ankigen.src.study.sample import Sample


def escape_str(text: str) -> str:
    return f'"{text.replace('"', '""')}"'


# todo escape html
def save_samples_as_anki(path: str, samples: Iterable[Sample], lang: str) -> None:
    with open(path, 'w', encoding='utf8') as file:
        for sample in samples:
            front = sample.text
            back_parts = [f'<a href="{get_translation_url(sample.text, lang)}">Translate</a>']
            if sample.source is not None:
                if validators.url(sample.source):
                    back_parts.append(f'<a href="{sample.source}">Source</a>')
                else:
                    back_parts.append(sample.source)
            if sample.english is not None:
                back_parts.append(sample.english)
            back = '<br><br>'.join(back_parts)
            file.write(f'{escape_str(front)};{escape_str(back)}\n')
