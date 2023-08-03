from pydantic import BaseModel


class DetailInfo(BaseModel):
    detail: str
