from fastapi import APIRouter

from app.routers.health import health_router
from app.routers.v1 import v1_router


app_router = APIRouter()

app_router.include_router(v1_router, prefix='/v1')
app_router.include_router(health_router, prefix='/health', tags=['Health'])
