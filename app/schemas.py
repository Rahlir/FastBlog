from datetime import datetime

from pydantic import BaseModel


class Post(BaseModel):
    title: str
    author: str
    content: str


class PostFull(Post):
    id: int
    timestamp_utc: datetime

    class Config:
        orm_mode = True
