from pydantic import BaseModel


class TagsDetail(BaseModel):
    id: int
    title: str
