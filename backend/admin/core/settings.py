import os

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file_encoding="utf-8",
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
    )
    # general
    DEBUG_MODE: bool = Field(default=False)
    ALLOWED_HOSTS: list[str] = Field(default=["*"])
    SECRET_APP: str | None = Field(default=None)

    # databse
    DATABASE_HOST: str | None = Field(default=None)
    DATABASE_NAME: str | None = Field(default=None)
    DATABASE_USER: str | None = Field(default=None)
    DATABASE_PASSWORD: str | None = Field(default=None)

    # cors
    CORS_ALLOWED_ORIGINS = list[str] = Field(default=["http://localhost"])

    # csrf
    CSRF_COOKIE_SECURE: bool = Field(default=False)
    CSRF_TRUSTED_ORIGINS: list[str | None] = Field(default=list())


settings = Settings()
