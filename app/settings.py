from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SENTRY_DSN: str | None = None
    CI: bool = False

    MONGODB_CONNECTION_STRING: str = 'mongodb://localhost:27017/test'

    @staticmethod
    def fastapi_docs_url() -> str:
        return '/docs'

    @staticmethod
    def fastapi_openapi_url() -> str:
        return '/openapi.json'


conf = Settings()
