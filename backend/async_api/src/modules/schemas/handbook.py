from datetime import datetime

from pydantic import Field
from pydantic import BaseModel
from pydantic import AliasChoices


"""
Данный блок представляет из себя схемы ответов на
конечные точки и не должны использоваться для валидации запросов
"""


class HBookPageDetail(BaseModel):
    id: int
    title: str


class SearchPageDetail(BaseModel):
    id: int
    title: str
    page_id: int
    page_title: str


class HBookContentDetail(BaseModel):
    title: str
    description: str
    page: list[HBookPageDetail] = Field(
        validation_alias=AliasChoices("page", "hbook_page")
    )


class HandbookDetail(BaseModel):
    id: int
    title: str
    description: str | None
    logo_url: str | None
    status: str | None


class HandbookDetailShort(BaseModel):
    id: int
    title: str
    description: str | None


class ContentDetail(HandbookDetailShort):
    content: list[HBookContentDetail]


class PageDetail(BaseModel):
    id: int
    meta: str
    title: str
    text: str
    reading_time: int
    create_date: datetime
    update_date: datetime


"""
Данный блок представляет из себя схемы запросов для валидации
на конечные точки и не должны использоваться для валидации ответов
"""


class SearchDetail(BaseModel):
    q: str = Field(min_length=1, max_length=80)
    handbook_id: int | None = Field(None, ge=1, le=2147483647)
    continue_after: int | None = Field(None, ge=1, le=100)
