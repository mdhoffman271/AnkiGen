from dataclasses import dataclass

from ankigen.src.study.lemmatization import LemmaCollection, Lemmatization


@dataclass(frozen=True)
class Interest:
    lemmas: LemmaCollection

    @staticmethod
    def from_text(text: str) -> 'Interest':
        return Interest(Lemmatization.from_text(text).unique())
