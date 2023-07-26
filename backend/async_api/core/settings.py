from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", env_file_encoding="utf-8"
    )
    DEBUG_MODE: bool = Field(default=False)

    URL_DATABASE: str

    ALLOW_ORIGINS: tuple[str] = Field(default=("*",))


settings = Settings()
