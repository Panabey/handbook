from datetime import datetime

from pydantic import BaseModel


class PostDetail(BaseModel):
    id: int
    title: str
    text: str
    reading_time: int
    create_date: datetime
    upload_date: datetime
