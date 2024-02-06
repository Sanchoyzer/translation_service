from app.models.translate import Translate
from app.repositories.base import BaseRepository


class TranslationRepository(BaseRepository[Translate]):
    class Meta:
        collection_name = 'translate'
        response_model = Translate

    async def create(self, translate: Translate) -> Translate:
        return await self.create_one(document=translate)

    async def get_list(
        self,
        page: int,
        page_size: int,
        sort: list[str] | None = None,
        searched_word: str | None = None,
    ) -> list[Translate]:
        return await self.get_paginated(
            criteria={'text': {'$regex': searched_word, '$options': 'i'}} if searched_word else {},
            page=page,
            page_size=page_size,
            sort=[((s[1:], -1) if s.startswith('-') else (s, 1)) for s in sort] if sort else None,
        )

    async def delete(self, criteria: dict) -> int:
        return await self.delete_many(criteria)


translation_repo = TranslationRepository()
