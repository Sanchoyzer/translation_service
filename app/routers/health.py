from datetime import UTC, datetime
from typing import Final

from fastapi import APIRouter

from app import __VERSION__
from app.repositories.translate import translation_repo


health_router: APIRouter = APIRouter()
started: Final[str] = datetime.now(tz=UTC).isoformat()


async def check_services_health() -> bool:
    return bool(await translation_repo.health())


@health_router.get('')
async def ready() -> dict[str, str]:
    await check_services_health()
    return {'up_since': started, 'version': __VERSION__}


@health_router.get('/failed')
async def failed() -> None:
    raise RuntimeError('test')
