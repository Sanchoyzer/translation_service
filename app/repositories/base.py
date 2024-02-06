from typing import Generic, TypeVar

from pydantic import TypeAdapter

from app.connections.mongo import MongoClient
from app.models.base import MongoBaseModel
from app.settings import conf


T = TypeVar('T', bound=MongoBaseModel)


class BaseRepository(Generic[T]):
    class Meta:
        collection_name: str
        response_model = MongoBaseModel

    def __init__(self) -> None:
        self.mongo_client = MongoClient(conf.MONGODB_CONNECTION_STRING)
        self.db = self.mongo_client.get_default_database()
        self.collection = self.db.get_collection(self.Meta.collection_name)

    @staticmethod
    def to_mongo(model: T) -> dict:
        return {'_id': model.id, **model.model_dump(exclude={'id'})}

    @staticmethod
    def from_mongo(response: dict) -> dict:
        return {'id': response['_id'], **response}

    async def count(self, criteria: dict) -> int:
        async with await self.mongo_client.start_session() as session:
            return await self.collection.count_documents(criteria, session=session)

    async def create_one(self, document: T) -> T:
        async with await self.mongo_client.start_session() as session:
            created_document = await self.collection.insert_one(
                self.to_mongo(document),
                session=session,
            )
            created_document = await self.collection.find_one(
                {'_id': created_document.inserted_id},
                session=session,
            )
            return TypeAdapter(self.Meta.response_model).validate_python(  # type: ignore[return-value]
                self.from_mongo(created_document),
            )

    async def get_paginated(
        self,
        criteria: dict,
        page: int,
        page_size: int,
        sort: list[tuple] | None = None,
    ) -> list[T]:
        async with await self.mongo_client.start_session() as session:
            document_list = (
                self.collection.find(criteria, sort=sort or [], session=session)
                .skip(page * page_size)
                .limit(page_size)
            )
            return [
                TypeAdapter(self.Meta.response_model).validate_python(self.from_mongo(doc))  # type: ignore[misc]
                async for doc in document_list
            ]

    async def get_one(
        self,
        criteria: dict,
        sort: list[tuple[str, int]] | None = None,
    ) -> T | None:
        async with await self.mongo_client.start_session() as session:
            doc = await self.collection.find_one(criteria, sort=sort or [], session=session)
            if not doc:
                return None
            return TypeAdapter(self.Meta.response_model).validate_python(self.from_mongo(doc))  # type: ignore[return-value]

    async def delete_many(self, criteria: dict) -> int:
        async with await self.mongo_client.start_session() as session:
            result = await self.collection.delete_many(criteria, session=session)
            return result.deleted_count

    async def health(self) -> dict:
        async with await self.mongo_client.start_session() as session:
            return await self.db.command({'dbstats': 1}, session=session)
