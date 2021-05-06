from typing import List

from fastapi import FastAPI, HTTPException
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
    """List all the blog posts in the database showing each post's details"""
    return db_session.get_all(PostModel)


@app.put("/blog/{post_id}", response_model=Post)
def edit_post(post_id: int, post_edits: PostEdit):
    """Edit blog post"""
    post_edits_model = PostModel(**post_edits.dict(exclude_unset=True))
    db_session.update(post_edits_model, post_id)
    updated = db_session.get(PostModel, post_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return updated


@app.delete("/blog/posts/{post_id}", response_model=Post)
def delete_post(post_id: int):
    """Delete blog post with the specified id"""
    deleted = db_session.delete(PostModel, post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return deleted


@app.get("/blog/posts/{post_id}", response_model=Post)
def post_details(post_id: int):
    """Get details of a blog post with the specified id"""
    details = db_session.get(PostModel, post_id)
    if not details:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return details


@app.get("/")
def index():
    """Redirect to docs"""
    return RedirectResponse("/docs")
