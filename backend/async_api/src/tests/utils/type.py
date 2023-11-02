from datetime import datetime


def pydantic_datetime(dt: datetime):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
