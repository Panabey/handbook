from datetime import datetime

from pydantic import Field
from pydantic import BaseModel
from pydantic import AliasChoices


class HBookPage(BaseModel):
    id: int
    title: str


class HBookContent(BaseModel):
    title: str
    page: list[HBookPage] = Field(validation_alias=AliasChoices("page", "hbook_page"))


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
    content: list[HBookContent]


class PageDetail(BaseModel):
    id: int
    title: str
    text: str
    reading_time: int
    create_date: datetime
    update_date: datetime
