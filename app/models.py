from datetime import datetime, timezone

from .database import DbModel


class PostModel(DbModel):
    def __init__(self, author=None, title=None, content=None, timestamp_utc=None):
        # This is a property of table created by this model - attribute of PostModel
        # used as a primary (and unique) key will be 'id'
        self.primary_key = 'id'

        self.author = author
        self.title = title
        self.content = content
        self.timestamp_utc = timestamp_utc

    @classmethod
    def new(cls, author: str, title: str, content: str):
        return cls(author, title, content, datetime.now(timezone.utc))
