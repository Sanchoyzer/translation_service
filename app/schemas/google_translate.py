from itertools import chain
from typing import Self

from pydantic import model_validator

from app.exceptions import MistakeInWordError
from app.schemas.base import ResponseModel


class TranslationExtraData(ResponseModel):
    definitions: dict[str, list[str]]
    synonyms: dict[str, list[str]]
    translations: dict[str, list[str]]
    examples: list[str]

    @model_validator(mode='before')
    @classmethod
    def cleanup_data(cls: type[Self], data: dict) -> dict:
        if mistakes := data.get('possible-mistakes'):
            raise MistakeInWordError(f'It looks like a mistake, maybe you meant "{mistakes[1]}"?')

        if in_definition := data.get('definitions'):
            definitions = {i[0]: [j[0] for j in i[1]] for i in in_definition}
            data['definitions'] = definitions

        if in_synonyms := data.get('synonyms'):
            synonyms = {i[0]: list(chain(*[j[0] for j in i[1]])) for i in in_synonyms}
            data['synonyms'] = synonyms

        if in_translations := data.get('all-translations'):
            translations = {i[0]: i[1] for i in in_translations}
            data['translations'] = translations

        if in_examples := data.get('examples'):
            examples = [
                j.replace('<b>', '').replace('</b>', '')
                for i in in_examples[0]
                for j in i[:-1]
                if j
            ]
            data['examples'] = examples
        return data


class TranslationSchema(ResponseModel):
    src: str
    dest: str
    origin: str
    text: str
    extra_data: TranslationExtraData
