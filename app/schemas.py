from typing import Optional
from datetime import datetime

from pydantic import BaseModel, validator


class PostRaw(BaseModel):
    """Base model for post which contains all possible fields"""
    title: Optional[str]
    author: Optional[str]
    content: Optional[str]
    id: Optional[int]
    timestamp_utc: Optional[datetime]


class PostEdit(PostRaw):
    """
    Not sure if there is more elegant solution, but this schema
    is necessary to ensure that by PUT edit requests don't try to modify
    id of a post
    """
    @validator('id')
    def id_unset(cls, v):
        assert v is None, "Id cannot be editted"


class PostNew(PostRaw):
    """For new posts title, author, and content are mandatory"""
    title: str
    author: str
    content: str


class Post(PostNew):
    """
    This is the Post schema corresponding to PostModel,
    which is how posts are stored in the FakeDb
    """
    id: int
    timestamp_utc: datetime

    class Config:
        orm_mode = True
