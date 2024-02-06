from typing import Final, Self

from app.models.translate import Translate
from app.repositories.translate import translation_repo
from app.schemas.translate import TranslateRequest
from app.services.google_translate import GoogleTranslateService


class TranslateService:
    @classmethod
    async def translate_word(cls: type[Self], data: TranslateRequest) -> Translate:
        in_data = data.model_dump()
        if translation := await translation_repo.get_one(criteria=in_data):
            return translation

        google_translation = await GoogleTranslateService.translate(**in_data)

        in_translation = Translate.model_validate(
            {
                'text': data.text,
                'src_lang': data.src_lang,
                'dest_lang': data.dest_lang,
                'definitions': google_translation.extra_data.definitions,
                'synonyms': google_translation.extra_data.synonyms,
                'translations': google_translation.extra_data.translations,
                'examples': google_translation.extra_data.examples,
            },
        )
        return await translation_repo.create_one(document=in_translation)

    @classmethod
    async def get_list_words(  # noqa: PLR0913
        cls: type[Self],
        page: int,
        page_size: int,
        sort: list[str] | None,
        searched_word: str | None,
        *,
        include_definition: bool,
        include_synonyms: bool,
        include_translations: bool,
    ) -> dict[str, list[dict]]:
        result = await translation_repo.get_list(
            page=page,
            page_size=page_size,
            sort=sort,
            searched_word=searched_word,
        )

        prefix: Final[str] = 'include_'
        exclude = {
            k.removeprefix(prefix)
            for k, v in locals().copy().items()
            if k.startswith(prefix) and not v
        }

        return {'items': [i.model_dump(exclude=exclude) for i in result]}

    @classmethod
    async def remove_word(cls: type[Self], word: str) -> None:
        word = word.split(maxsplit=1)[0]
        await translation_repo.delete({'text': word})
