from typing import TextIO


def escape_str(text: str) -> str:
    return f'"{text.replace('"', '""')}"'


def save_dict_as_anki(path: str, data: dict[str, str]) -> None:
    with open(path, 'w', encoding='utf8') as file:
        for key, value in data.items():
            file.write(f'{escape_str(key)};{escape_str(value)}\n')
