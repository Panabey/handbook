import os

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

BASE_URL = os.path.dirname(os.path.dirname(__file__))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file_encoding="utf-8",
        env_file=(os.path.join(BASE_URL, ".env"), ".env"),
    )
    # general
    DEBUG_MODE: bool = Field(default=False)
    ALLOWED_HOSTS: list[str] = Field(default=["*"])
    SECRET_APP: str | None = Field(default=None)

    # databse
    DATABASE_HOST: str

    DB_BACKEND_NAME: str
    DB_BACKEND_USER: str
    DB_BACKEND_PASSWORD: str

    DB_ADMIN_NAME: str
    DB_ADMIN_USER: str
    DB_ADMIN_PASSWORD: str

    # cors
    CORS_ALLOWED_ORIGINS: list[str] = Field(default=["http://localhost"])

    # csrf
    CSRF_COOKIE_SECURE: bool = Field(default=False)
    CSRF_TRUSTED_ORIGINS: list[str | None] = Field(default=list())
    # session
    SESSION_COOKIE_SECURE: bool = Field(default=False)


settings = Settings()
