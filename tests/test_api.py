import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope='module')
def client():
    return TestClient(app)


@pytest.fixture
def sample_post():
    return {
        "author": "Tadeas Uhlir",
        "title": "Sample Post",
        "content": "Lorem ipsum dolor sit amet"
    }


def post_equality(post1, post2):
    return (post1["id"] == post2["id"] and post1["author"] == post2["author"]
            and post1["title"] == post2["title"] and post1["content"] == post2["content"])


def test_firstadd(client, sample_post):
    ex_id = 1
    response = client.post("/blog/posts", json=sample_post)
    assert response.status_code == 200
    # Populate sample_post with expected id
    sample_post["id"] = ex_id
    assert post_equality(sample_post, response.json())


def test_secondadd(client, sample_post):
    ex_id = 2
    response = client.post("/blog/posts", json=sample_post)
    assert response.status_code == 200
    # Populate sample_post with expected id
    sample_post["id"] = ex_id
    assert post_equality(sample_post, response.json())


def test_get(client):
    existant_id = 1
    nonexistant_id = 3

    response = client.get(f"/blog/posts/{existant_id}")
    assert response.status_code == 200

    response = client.get(f"/blog/posts/{nonexistant_id}")
    assert response.status_code == 404


def test_delete(client, sample_post):
    ex_id = 3
    sample_post["author"] = "Jon Doe"
    sample_post["title"] = "Groundbreaking Discovery"
    response = client.post("/blog/posts", json=sample_post)
    # Populate sample_post with expected id
    sample_post["id"] = ex_id
    # Check id is as expected
    assert response.json()["id"] == sample_post["id"]

    # Check entry is in the database
    get_response = client.get(f"/blog/posts/{ex_id}")
    assert post_equality(get_response.json(), sample_post)

    # Delete entry
    del_response = client.delete(f"/blog/posts/{ex_id}")
    assert del_response.status_code == 200
    assert post_equality(del_response.json(), sample_post)
    # See if it's deleted
    get_response = client.get(f"/blog/posts/{ex_id}")
    assert get_response.status_code == 404


def test_getall(client):
    # There should now be two entries
    response = client.get("/blog/posts")
    assert len(response.json()) == 2
