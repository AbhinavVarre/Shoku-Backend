from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app, get_db

import os
from dotenv import load_dotenv

load_dotenv()

host     = os.getenv('HOST')
user     = os.getenv('DBUSER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
port     = os.getenv('PORT')

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        if db:
            db.close()


app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)

def test_create_user(client):
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
