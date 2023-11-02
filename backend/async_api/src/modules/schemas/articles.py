from datetime import datetime

from pydantic import Field
from pydantic import BaseModel
from pydantic import AliasChoices
from pydantic import field_validator

from .tags import TagsDetail

"""
Данный блок представляет из себя схемы ответов на
конечные точки и не должны использоваться для валидации запросов
"""


class ArticleDetail(BaseModel):
    id: int
    title: str
    anons: str
    text: str
    tags: list[str] = Field(validation_alias=AliasChoices("tags", "tags_article_info"))
    reading_time: int
    create_date: datetime
    update_date: datetime

    @field_validator("tags", mode="before")
    @classmethod
    def tags_to_list(cls, v: list[TagsDetail]) -> list[str]:
        return [tag.title for tag in v]


class ArticleShortDetail(BaseModel):
    id: int
    logo_url: str | None
    title: str
    anons: str
    tags: list[str] = Field(validation_alias=AliasChoices("tags", "tags_article_info"))
    reading_time: int
    create_date: datetime

    @field_validator("tags", mode="before")
    @classmethod
    def tags_to_list(cls, v: list[TagsDetail]) -> list[str]:
        return [tag.title for tag in v]


class ArticleAllDetail(BaseModel):
    items: list[ArticleShortDetail]
    current_page: int
    total_page: int


"""
Данный блок представляет из себя схемы запросов для валидации
на конечные точки и не должны использоваться для валидации ответов
"""


class SearchDetail(BaseModel):
    q: str | None = Field(None, min_length=1, max_length=120)
    limit: int = Field(default=20, ge=1, le=20)
    tags: list[int] = Field(max_length=4)
    continue_after: int | None = Field(default=None, ge=1, le=1000)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, tags: list[int]):
        if not tags:
            return tags

        for value in tags:
            if not 1 <= value <= 2147483647:
                raise ValueError(
                    "значение должно быть в диапазоне между 1 и 2147483647"
                )
        return tags
