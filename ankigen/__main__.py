from ankigen.src.study.anki_bulider import AnkiBuilder


def main():
    for lang in ['de', 'es', 'fr']:
        builder = (
            AnkiBuilder(lang)
            .with_epub(f'./data/epub/{lang}/**/*.epub')
            .with_kaikki('./data/kaikki/raw-wiktextract-data.jsonl.gz')
            .with_text(f'./data/text/{lang}/**/*.txt')
            .with_firefox_wiktionary('./data/firefox/places.sqlite', 61.0)
        )
        builder.generate('./data/out/')


main()
