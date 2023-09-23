from datetime import datetime

from pydantic import Field, field_validator
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


class HandbookStatusDetail(BaseModel):
    title: str
    color_text: str
    color_background: str


class HandbookDetail(BaseModel):
    id: int
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


class HandbookDetailShort(BaseModel):
    id: int
    title: str
    description: str | None


class ContentDetail(HandbookDetailShort):
    content: list[HBookContentDetail]


class PageDetail(BaseModel):
    id: int
    short_description: str
    title: str
    text: str
    reading_time: int
    create_date: datetime
    update_date: datetime
    handbook: HBookPageDetail = Field(
        validation_alias=AliasChoices("handbook", "hbook_content")
    )

    @field_validator("handbook", mode="before")
    @classmethod
    def content_to_handbook(cls, v) -> HBookPageDetail:
        return v.hbook


"""
Данный блок представляет из себя схемы запросов для валидации
на конечные точки и не должны использоваться для валидации ответов
"""


class SearchDetail(BaseModel):
    q: str = Field(min_length=1, max_length=80)
    handbook_id: int | None = Field(None, ge=1, le=2147483647)
    limit: int = Field(15, ge=1, le=15)
    continue_after: int | None = Field(None, ge=1, le=100)
