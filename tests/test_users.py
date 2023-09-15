from app import schemas
from .database import client, session


def test_create_user(client, session):
    response = client.post(
        "/users/add",
        json={"name": "abhinav", "password": "chimichangas"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "name" in data
    assert data["name"] == "abhinav"
    user_name = data["name"]

    response = client.get(f"/users/name/{user_name}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "abhinav"
    assert data["name"] == user_name