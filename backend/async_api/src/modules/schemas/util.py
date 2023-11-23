from datetime import datetime

from pydantic import Field
from pydantic import BaseModel
from pydantic import AliasChoices
from pydantic import field_validator


class DetailHandbooks(BaseModel):
    id: int
    title: str
    update_date: datetime
    handbook_slug: str = Field(
        validation_alias=AliasChoices("handbook_title", "hbook_content")
    )
    handbook_title: str = Field(
        validation_alias=AliasChoices("handbook_title", "hbook_content")
    )

    @field_validator("handbook_slug", mode="before")
    @classmethod
    def get_handbook_slug(cls, value) -> str:
        return value.hbook.slug

    @field_validator("handbook_title", mode="before")
    @classmethod
    def get_handbook_title(cls, value) -> str:
        return value.hbook.title


class DetailArticles(BaseModel):
    id: int
    title: str
    update_date: datetime


class DetailSitemap(BaseModel):
    handbooks: list[DetailHandbooks]
    articles: list[DetailArticles]
