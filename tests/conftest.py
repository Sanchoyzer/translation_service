import asyncio
from asyncio import AbstractEventLoop
from collections.abc import AsyncIterator, Generator

import pytest
import pytest_asyncio
from faker import Faker

from app.connections.mongo import MongoClient
from app.settings import conf


@pytest.fixture(scope='session')
def faker():
    return Faker()


@pytest.fixture(scope='session')
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def mongo_client() -> MongoClient:
    return MongoClient(conf.MONGODB_CONNECTION_STRING)


@pytest_asyncio.fixture(autouse=True)
async def collections_cleanup(mongo_client) -> AsyncIterator[None]:
    await mongo_client.drop_all_collections()
    yield
    await mongo_client.drop_all_collections()
