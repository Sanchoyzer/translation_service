import sentry_sdk
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.httpx import HttpxIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration


def setup_sentry(
    dsn: str | None,
    rate: float = 1.0,
    ignore_errors: list[type | str] | None = None,
) -> None:
    if not dsn:
        return
    ignore_errors = ignore_errors or []
    integrations = [
        StarletteIntegration(),
        FastApiIntegration(),
        HttpxIntegration(),
        AsyncioIntegration(),
    ]
    sentry_sdk.init(
        dsn=dsn,
        integrations=integrations,
        traces_sample_rate=rate,
        ignore_errors=ignore_errors,
    )
