import os

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

# Базовый путь к файлу переменных окружения
BASE_URL = os.path.dirname(os.path.dirname(__file__))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file_encoding="utf-8",
        env_file=(os.path.join(BASE_URL, ".env"), ".env"),
    )
    # Рсновная конфигурация
    DEBUG_MODE: bool = False

    # PostgreSQL database
    URL_DATABASE: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int = 6379

    # Docs
    OPEN_API_URL: str | None = "/openapi.json"
    DOCS_URL: str | None = "/docs"
    REDOC_URL: str | None = "/redoc"


settings = Settings()  # type: ignore
