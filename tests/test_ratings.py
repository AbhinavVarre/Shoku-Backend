from app import schemas
from .database import client, session
import json


from app import schemas
from .database import client, session
from uuid import uuid4

from app import schemas
from .database import client, session
from uuid import uuid4
import json

def test_create_rating(client, session):
    # Create a user
    user_name = f"test_user_{uuid4()}"
    response = client.post(
        "/users/add",
        json=schemas.UserCreate(name=user_name, password="test_password").model_dump(),
    )
    assert response.status_code == 200, response.text

    # Log in as the user and retrieve the access token
    response = client.post(
        "/login",
        data={
            "username": user_name,
            "password": "test_password"
        }
    )
    assert response.status_code == 200, response.text
    access_token = response.json()["access_token"]

    # Create a restaurant
    restaurant_name = f"test_restaurant_{uuid4()}"
    response = client.post(
        "/restaurants/add",
        json=schemas.RestaurantCreate(name=restaurant_name).model_dump(),
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "name" in data
    assert data["name"] == restaurant_name
    restaurant_id = data["id"]

    # Submit a rating for the restaurant with the authorized access token
    response = client.post(
        "/ratings/new",
        data={
            "item_json": json.dumps(schemas.RatingCreate(
                restaurant_name=restaurant_name,
                score=4,
                review="test_comment"
            ).model_dump())
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {access_token}"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "restaurant_id" in data
    assert data["restaurant_id"] == restaurant_id
    assert "score" in data
    assert data["score"] == 4
    assert "review" in data
    assert data["review"] == "test_comment"
