from datetime import datetime

from pydantic import Field
from pydantic import BaseModel
from pydantic import AliasChoices
from pydantic import field_validator


class MyProfileDetail(BaseModel):
    id: int
    avatar_url: str
    name: str
    is_active: bool
    registration_date: datetime
    user_id: int
    oauth_service: str = Field(
        validation_alias=AliasChoices("oauth_service", "service_info")
    )

    @field_validator("oauth_service", mode="before")
    @classmethod
    def get_handbook_slug(cls, value) -> str:
        return value.service_name


class AuthorProfileDetail(BaseModel):
    id: int
    avatar_url: str
    name: str
    registration_date: datetime
