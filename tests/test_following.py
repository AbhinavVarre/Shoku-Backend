from app import schemas
from .database import client, session
from app import schemas
from .database import client, session
from uuid import uuid4

from app import schemas
from .database import client, session
from uuid import uuid4


def test_following(client, session):
    # Create first user
    user1_name = f"test_user_{uuid4()}"
    response = client.post(
        "/users/add",
        json=schemas.UserCreate(name=user1_name, password="test_password").model_dump(),
    )
    assert response.status_code == 200, response.text
    user1_id = response.json()["id"]

    # Create second user
    user2_name = f"test_user_{uuid4()}"
    response = client.post(
        "/users/add",
        json=schemas.UserCreate(name=user2_name, password="test_password").model_dump(),
    )
    assert response.status_code == 200, response.text
    user2_id = response.json()["id"]

    # Login as first user
    response = client.post(
        "/login", data={"username": user1_name, "password": "test_password"}
    )
    assert response.status_code == 200, response.text
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Follow second user
    response = client.post(f"/users/follow/{user2_name}", headers=headers)
    assert response.status_code == 200, response.text

    # Check that first user's following list contains second user
    response = client.get("/users/following", headers=headers)
    assert response.status_code == 200, response.text
    following = response.json()
    assert len(following) == 1
    assert following[0]["id"] == user2_id

    # Login as second user
    response = client.post(
        "/login", data={"username": user2_name, "password": "test_password"}
    )
    assert response.status_code == 200, response.text
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Check that second user's followers list contains first user
    response = client.get("/users/followers", headers=headers)
    assert response.status_code == 200, response.text
    followers = response.json()
    assert len(followers) == 1
    assert followers[0]["id"] == user1_id
