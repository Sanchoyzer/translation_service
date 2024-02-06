from app.models.base import MongoBaseModel


class Translate(MongoBaseModel):
    text: str
    src_lang: str
    dest_lang: str
    definitions: dict[str, list[str]]
    synonyms: dict[str, list[str]]
    translations: dict[str, list[str]]
    examples: list[str]
