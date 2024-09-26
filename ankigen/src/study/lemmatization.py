from __future__ import annotations

from dataclasses import dataclass

from ankigen.src.study.context import ActiveContext

LemmaCollection = tuple[str, ...]


@dataclass(frozen=True)
class Lemmatization:
    lemmas: LemmaCollection

    def unique(self) -> LemmaCollection:
        return tuple(sorted(set(self.lemmas)))

    @staticmethod
    def from_text(context: ActiveContext, text: str) -> Lemmatization:
        return Lemmatization(tuple(context.iter_lemmas(text)))
