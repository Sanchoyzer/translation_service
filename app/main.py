from fastapi import FastAPI

from app import __VERSION__
from app.connections.sentry import setup_sentry
from app.middleware import CatchExceptionMiddleware
from app.routers import app_router
from app.settings import conf


def init_app(*, testing: bool = False) -> FastAPI:
    if conf.SENTRY_DSN and not conf.CI and not testing:
        setup_sentry(dsn=conf.SENTRY_DSN)

    app = FastAPI(
        title='Translation Service Challenge',
        version=__VERSION__,
        docs_url=conf.fastapi_docs_url(),
        openapi_url=conf.fastapi_openapi_url(),
    )

    app.add_middleware(CatchExceptionMiddleware)

    app.include_router(router=app_router)

    return app
