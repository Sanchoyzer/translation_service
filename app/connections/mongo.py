from motor.motor_asyncio import AsyncIOMotorClient


class MongoClient(AsyncIOMotorClient):  # type: ignore[valid-type,misc]
    def __init__(self, mongodb_connection_string: str) -> None:
        super().__init__(
            host=mongodb_connection_string,
            uuidRepresentation='standard',
            tz_aware=True,
        )

    async def drop_all_collections(self) -> None:
        db = self.get_default_database()
        for collection_name in await db.list_collection_names():
            await db[collection_name].drop()
