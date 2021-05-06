import pytest

import app.database as db
from app.models import PostModel


@pytest.fixture(scope='module')
def db_connect():
    return db.session_connect()


@pytest.fixture
def sample_post():
    author = "Tadeas Uhlir"
    title = "Sample Post"
    content = "Lorem ipsum dolor sit amet"

    return PostModel.new(author, title, content)


def test_firstadd(db_connect, sample_post):
    ex_id = 1
    db_connect.add(sample_post)

    assert sample_post.id == ex_id

    retrieve = db_connect.get(PostModel, 1)

    assert retrieve == sample_post


def test_secondadd(db_connect, sample_post):
    ex_id = 2
    db_connect.add(sample_post)

    assert sample_post.id == ex_id

    retrieve = db_connect.get(PostModel, 2)

    assert retrieve == sample_post


def test_delete(db_connect, sample_post):
    ex_id = 3
    sample_post.title = "Sample Post to Delete"
    db_connect.add(sample_post)

    assert db_connect.get(PostModel, ex_id) == sample_post

    res = db_connect.delete(PostModel, ex_id)

    assert len(db_connect.get_all(PostModel)) == 2
    assert db_connect.get(PostModel, ex_id) is None
    assert res == sample_post


def test_update(db_connect, sample_post):
    ex_id = 4
    sample_post.title = "Sample Post to Edit"
    db_connect.add(sample_post)
    assert sample_post.id == ex_id

    edits_post = PostModel(content="We updated the content", author="Group")
    db_connect.update(edits_post, ex_id)
    updated_post = db_connect.get(PostModel, ex_id)
    assert updated_post != sample_post
    assert updated_post.title == sample_post.title
    assert updated_post.timestamp_utc == sample_post.timestamp_utc
    assert updated_post.content == edits_post.content
    assert updated_post.author == edits_post.author
