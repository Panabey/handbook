from datetime import datetime

from pydantic import BaseModel


"""
Данный блок представляет из себя схемы ответов на
конечные точки и не должны использоваться для валидации запросов
"""


class NewsDetail(BaseModel):
    id: int
    title: str
    text: str
    reading_time: int
    create_date: datetime


class NewsShortDetail(BaseModel):
    id: int
    title: str
    reading_time: int
    create_date: datetime


class NewsAllDetail(BaseModel):
    items: list[NewsShortDetail]
    current_page: int
    total_page: int


class NewsWidgetDetail(BaseModel):
    id: int
    title: str
    create_date: datetime
