from ankigen.src.study.anki_bulider import AnkiBuilder
from ankigen.src.study.context import Context

# todo cli


def main():
    for lang in ['de', 'es', 'fr']:
        with Context(lang) as context:
            path = f'./data/out/{lang}.txt'

            anki = (
                AnkiBuilder(context, log_func=print)
                .with_epub(f'./data/epub/{lang}/**/*.epub')
                .with_kaikki('./data/kaikki/raw-wiktextract-data.jsonl.gz')
                .with_text(f'./data/text/{lang}/**/*.txt')
                .with_firefox_wiktionary('./data/firefox/places.sqlite', 61.0)
                .build()
            )

            print(f"saving samples to '{path}' ...")
            anki.save(path)

            print('listing unsatisfied interests ...')
            for interest in anki.unsatisfied_interests():
                print('\t', interest)


main()
