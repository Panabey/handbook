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
    subpart: int
    title: str


class SearchPageDetail(BaseModel):
    id: int
    slug: str
    title: str
    page_id: int
    page_title: str


class HBookContentDetail(BaseModel):
    part: int
    title: str
    description: str
    page: list[HBookPageDetail] = Field(
        validation_alias=AliasChoices("page", "hbook_page")
    )


class HandbookStatusDetail(BaseModel):
    title: str
    color_text: str
    color_background: str


class HandbookDetail(BaseModel):
    id: int
    slug: str
    title: str
    logo_url: str | None
    status: HandbookStatusDetail | None = Field(
        validation_alias=AliasChoices("status", "status_info")
    )


class CategoryDetail(BaseModel):
    title: str
    handbook: list[HandbookDetail] = Field(
        validation_alias=AliasChoices("handbook", "hbook_category")
    )


class HandbookDetailUShort(BaseModel):
    id: int
    slug: str
    title: str


class HandbookDetailShort(BaseModel):
    id: int
    slug: str
    title: str
    description: str | None


class BookMaterial(BaseModel):
    logo_url: str | None
    title: str
    author: str


class ContentDetail(HandbookDetailShort):
    content: list[HBookContentDetail]
    books: list[BookMaterial] | None = Field(
        validation_alias=AliasChoices("books", "book_info")
    )


class PageInfoDetail(BaseModel):
    part: int
    handbook: HandbookDetailUShort = Field(
        validation_alias=AliasChoices("handbook", "hbook")
    )


class PageDetail(BaseModel):
    id: int
    short_description: str
    subpart: int
    title: str
    text: str
    reading_time: int
    create_date: datetime
    update_date: datetime
    content: PageInfoDetail = Field(
        validation_alias=AliasChoices("content", "hbook_content")
    )


"""
Данный блок представляет из себя схемы запросов для валидации
на конечные точки и не должны использоваться для валидации ответов
"""


class SearchDetail(BaseModel):
    q: str = Field(min_length=1, max_length=80)
    handbook_id: int | None = Field(None, ge=1, le=2147483647)
    limit: int = Field(15, ge=1, le=15)
    continue_after: int | None = Field(None, ge=1, le=100)
