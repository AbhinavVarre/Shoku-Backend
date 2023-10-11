from app import schemas
from .database import client, session
from uuid import uuid4
import json

def test_following(client, session):
    # create two users
    user1 = schemas.UserCreate(name="user1", password="password1")
    user2 = schemas.UserCreate(name="user2", password="password2")
    response = client.post("/users/add", json=user1.model_dump())
    assert response.status_code == 200
    assert response.json()["name"] == user1.name
    response = client.post("/users/add", json=user2.model_dump())
    assert response.status_code == 200
    assert response.json()["name"] == user2.name

    # log in as first user
    response = client.post("/login", data={"username": user1.name, "password": user1.password})
    assert response.status_code == 200
    assert "access_token" in response.json()
    token = response.json()["access_token"]

    # create restaurant
    restaurant = schemas.RestaurantCreate(name="restaurant1")
    response = client.post("/restaurants/add", json=restaurant.model_dump(), headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == restaurant.name
    restaurant_id = response.json()["id"]

    # create list
    restaurant_list = schemas.RestaurantListCreate(name="list1", description="description1")
    response = client.post("/restaurantlist/add", data={"list_json": json.dumps(restaurant_list.model_dump())}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == restaurant_list.name
    list_name = response.json()["name"]

    # add restaurant to list
    response = client.post(f"/restaurantlist/{list_name}/add/{restaurant.name}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == list_name

    # share list with other user
    response = client.post(f"/restaurantlist/{list_name}/share/{user2.name}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == list_name

    # log in as second user
    response = client.post("/login", data={"username": user2.name, "password": user2.password})
    assert response.status_code == 200
    assert "access_token" in response.json()
    token = response.json()["access_token"]

    # see if list appears
    response = client.get("/restaurantlist/all", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert any(list["name"] == list_name for list in response.json())
    