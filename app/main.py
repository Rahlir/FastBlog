from fastapi import FastAPI

from app.schemas import Post, PostFull
from app.models import PostModel
from app.database import session_connect

app = FastAPI()
db_session = session_connect()


@app.get("/")
def root():
    """Something like a doc maybe?"""
    return {"message": "Hello World"}


@app.post("/blog/posts/", response_model=PostFull)
def create_post(new_post: Post):
    """Create a new blog post"""
    pass


def edit_post():
    pass


def delete_post():
    pass


@app.get("/blog/posts")
def list_posts():
    pass


@app.get("/blog/posts/{post_id}", response_model=PostFull)
def post_details(post_id: int):
    """Get details of a blog post"""
    pass
