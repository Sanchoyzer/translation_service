import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.fixture(scope='session')
def path_() -> str:
    return '/health'


@pytest.mark.asyncio()
async def test_health(client: AsyncClient, path_: str) -> None:
    r = await client.get(path_)
    assert r.status_code == status.HTTP_200_OK, r.text
    assert (r_json := r.json()) and r_json.keys() == {'up_since', 'version'}
