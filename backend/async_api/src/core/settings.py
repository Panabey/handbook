import os

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

BASE_URL = os.path.dirname(os.path.dirname(__file__))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file_encoding="utf-8",
        env_file=os.path.join(BASE_URL, ".env"),
    )
    DEBUG_MODE: bool = Field(default=False)

    URL_DATABASE: str

    ALLOW_ORIGINS: tuple[str] = Field(default=("*",))


settings = Settings()
