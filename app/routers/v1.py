from fastapi import APIRouter

from app.routers.translate import translate_router


v1_router = APIRouter()

v1_router.include_router(translate_router, prefix='/translate', tags=['Translation'])
