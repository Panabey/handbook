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
    # Основные параметры
    DEBUG_MODE: bool = False
    ALLOWED_HOSTS: list[str] = ["*"]
    SECRET_APP: str | None = None

    # Параметры Redis
    REDIS_HOST: str
    REDIS_PORT: int = 6379

    # Параметры БД
    DATABASE_HOST: str | None = None

    # Параметры внешней БД
    DB_BACKEND_NAME: str | None = None
    DB_BACKEND_USER: str | None = None
    DB_BACKEND_PASSWORD: str | None = None

    # Параметры БД по умолчанию
    DB_ADMIN_NAME: str | None = None
    DB_ADMIN_USER: str | None = None
    DB_ADMIN_PASSWORD: str | None = None

    # CORS параметры
    CORS_ALLOWED_ORIGINS: list[str] = ["http://localhost"]

    # CSRF параметры
    CSRF_COOKIE_SECURE: bool = False
    CSRF_TRUSTED_ORIGINS: list[str | None] = []

    # Session параметры
    SESSION_COOKIE_SECURE: bool = False

    # Внешний модуль axes security
    AXES_CLEAR_DATA: bool = True
    AXES_DISABLE_ACCESS_LOG: bool = True

    # Внешний модуль admin logs
    ADMIN_LOGS_ENABLED: bool = False


settings = Settings()
