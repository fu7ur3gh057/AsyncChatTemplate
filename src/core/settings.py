import enum
from typing import ClassVar, List

from pydantic_settings import BaseSettings
from yarl import URL


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    WORKERS_COUNT: int = 4
    HOST: str = "0.0.0.0"
    PORT: int = 8500
    RELOAD: bool = True
    BASE_URL: str
    SECRET_KEY: str
    WS_PATH: str
    CHAT_NAMESPACE_PATH: str
    DATABASE_URL: str
    REDIS_URL: str
    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str
    GOOGLE_API_KEY: str
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISHABLE_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    SENTRY_DNS: str
    SENTRY_SAMPLE_RATE: float = 0.2
    FIREBASE_CREDENTIALS_PATH: str
    DEBUG: bool
    ENVIRONMENT: str = "dev"
    LOG_LEVEL: LogLevel = LogLevel.INFO

    CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
    ]

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgres",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    @property
    def taskiq_broker_url(self) -> str:
        return self.REDIS_URL

    @property
    def taskiq_result_backend_url(self) -> str:
        return self.REDIS_URL

    class Config:
        env_file = ".env"


settings = Settings()
