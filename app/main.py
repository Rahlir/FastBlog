from typing import List

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.schemas import Post, PostNew, PostEdit
from app.models import PostModel
from app.database import session_connect

app = FastAPI()
db_session = session_connect()


@app.post("/blog/posts", response_model=Post)
def create_post(new_post: PostNew):
    """Create a new blog post"""
    new_post_model = PostModel.new(**new_post.dict(exclude_unset=True))
    db_session.add(new_post_model)
    return new_post_model


@app.get("/blog/posts", response_model=List[Post])
def list_posts():
    return db_session.get_all(PostModel)


@app.put("/blog/{post_id}", response_model=Post)
def edit_post(post_id: int, post_edits: PostEdit):
    post_edits_model = PostModel(**post_edits.dict(exclude_unset=True))
    db_session.update(post_edits_model, post_id)
    return db_session.get(PostModel, post_id)


@app.delete("/blog/posts/{post_id}", response_model=Post)
def delete_post(post_id: int):
    return db_session.delete(PostModel, post_id)


@app.get("/blog/posts/{post_id}", response_model=Post)
def post_details(post_id: int):
    """Get details of a blog post"""
    return db_session.get(PostModel, post_id)


@app.get("/")
def index():
    """Redirect to docs"""
    return RedirectResponse("/docs")
