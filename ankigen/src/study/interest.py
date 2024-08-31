
from dataclasses import dataclass
from ankigen.src.language.sentence import UniqueLemmaVector, unique_lemma_vector


@dataclass(frozen=True)
class Interest:
    lang: str
    lemmas: UniqueLemmaVector

    @staticmethod
    def from_text(text: str, lang: str) -> 'Interest':
        return Interest(lang, unique_lemma_vector(text, lang))
