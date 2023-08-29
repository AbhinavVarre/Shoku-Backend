from fastapi.testclient import TestClient
from app.main import app
from app import schemas


client = TestClient(app)

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    print(response.json())
