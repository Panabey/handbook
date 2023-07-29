from datetime import datetime

from pydantic import Field
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import AliasChoices


class HBookPage(BaseModel):
    id: int
    title: str
    slug: str


class HandbookDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None


class ContentDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    page: list[HBookPage] = Field(validation_alias=AliasChoices("page", "hbook_page"))


class PageDetail(BaseModel):
    id: int
    title: str
    slug: str
    text: str
    reading_time: int
    create_date: datetime
    update_date: datetime
