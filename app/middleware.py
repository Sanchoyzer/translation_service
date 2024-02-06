from fastapi import Request, status
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint, Response
from starlette.responses import JSONResponse

from app.exceptions import ClientError, MistakeInWordError, ServerError
from app.settings import conf


class CatchExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:  # noqa: BLE001
            match exc:
                case ValueError():
                    raise
                case ValidationError():
                    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                case MistakeInWordError():
                    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                case ClientError():
                    status_code = status.HTTP_400_BAD_REQUEST
                case ServerError():
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                case _:
                    if not conf.SENTRY_DSN:
                        # TODO: use logger
                        pass
                    raise
            content = {
                'detail': [{'loc': [], 'msg': str(exc), 'type': type(exc).__name__}],
            }
            return JSONResponse(status_code=status_code, content=content)
