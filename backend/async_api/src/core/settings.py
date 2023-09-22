import os

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

# Базовый путь к файлу конфигурации
BASE_URL = os.path.dirname(os.path.dirname(__file__))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file_encoding="utf-8",
        env_file=(os.path.join(BASE_URL, ".env"), ".env"),
    )
    # general
    DEBUG_MODE: bool = False

    # database
    URL_DATABASE: str

    # docs
    OPEN_API_URL: str | None = "/openapi.json"
    DOCS_URL: str | None = "/docs"
    REDOC_URL: str | None = "/redoc"


settings = Settings()
