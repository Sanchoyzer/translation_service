from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient

from app.main import init_app


@pytest.fixture(scope='session')
def asgi_app() -> FastAPI:
    return init_app(testing=True)


@pytest_asyncio.fixture()
async def client(asgi_app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(app=asgi_app, base_url='http://testserver') as aclient:
        yield aclient
