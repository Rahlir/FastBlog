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
        """Create a new blog post with the current timestamp.
        This will only create the model object, NOT
        save it in the database. That must be done separately

        Parameters
        ----------
        author : the author of the blog post
        title : the title of the blog post
        content : content (body) of the blog post

        Returns
        -------
        model object representing the blog post
        """

        return cls(author, title, content, datetime.now(timezone.utc))
