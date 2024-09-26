from ankigen.src.study.anki_bulider import AnkiBuilder
from ankigen.src.study.context import Context

# todo cli


def main():
    for lang in ['de', 'es', 'fr']:
        with Context(lang) as context:
            (
                AnkiBuilder(context)
                .with_epub(f'./data/epub/{lang}/**/*.epub')
                .with_kaikki('./data/kaikki/raw-wiktextract-data.jsonl.gz')
                .with_text(f'./data/text/{lang}/**/*.txt')
                .with_firefox_wiktionary('./data/firefox/places.sqlite', 61.0)
                .generate(f'./data/out/{lang}.txt')
            )


main()
