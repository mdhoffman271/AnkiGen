from dataclasses import dataclass

from ankigen.src.study.context import ActiveContext

LemmaCollection = tuple[str, ...]


@dataclass(frozen=True)
class Lemmatization:
    lemmas: LemmaCollection

    def unique(self) -> LemmaCollection:
        return tuple(sorted(set(self.lemmas)))

    @staticmethod
    def from_text(text: str) -> 'Lemmatization':
        return Lemmatization(tuple(ActiveContext.iter_lemmas(text)))
