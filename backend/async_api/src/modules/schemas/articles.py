from datetime import datetime

from pydantic import Field
from pydantic import BaseModel
from pydantic import AliasChoices


"""
Данный блок представляет из себя схемы ответов на
конечные точки и не должны использоваться для валидации запросов
"""


class TagsDetail(BaseModel):
    id: int
    title: str


class ArticleDetail(BaseModel):
    id: int
    title: str
    text: str
    tags: list[TagsDetail] = Field(
        validation_alias=AliasChoices("tags", "tags_article_info")
    )
    reading_time: int
    create_date: datetime
    update_date: datetime


class ArticleShortDetail(BaseModel):
    id: int
    title: str


class ArticleAllDetail(BaseModel):
    id: int
    logo_url: str | None
    title: str
    anons: str
    tags: list[TagsDetail] = Field(
        validation_alias=AliasChoices("tags", "tags_article_info")
    )
    reading_time: int
    create_date: datetime


class ArticleAllDetail(BaseModel):
    items: list[ArticleAllDetail]
    current_page: int
    total_page: int


"""
Данный блок представляет из себя схемы запросов для валидации
на конечные точки и не должны использоваться для валидации ответов
"""


class SearchDetail(BaseModel):
    q: str | None = Field(None, min_length=1, max_length=80)
    limit: int = Field(default=20, ge=1, le=20)
    continue_after: int | None = Field(default=None, ge=1, le=1000)
