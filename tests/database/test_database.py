from fastapi.testclient import TestClient
from main import app, get_db
from tests.database.session_test_db import TestingSessionLocal, engine

from database.models import model_metadata

for meta in model_metadata:
    meta.create_all(bind=engine)
    ...

# def init_db():
#     db = TestingSessionLocal()

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users/",
        json={
            "email": "deadpool@example.com",
            "password": "chimichangas4life"
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    # assert "id" in data
    # user_id = data["id"]

    # response = client.get(f"/users/{user_id}")
    # assert response.status_code == 200, response.text
    # data = response.json()
    # assert data["email"] == "deadpool@example.com"
    # assert data["id"] == user_id

def test_update_user():
    response = client.put(
        "/users/",
        json={
            "user_data": {
                "username":"oldusername",
                "password":"oldpassword"
                },
            "first_name":"new",
            "last_name":"NaMe",
            "email":"new@email.com",
            "password":"newpassword",
            }
        )
    data = response.json()
    assert data["data"]["email"] == "new@email.com"
    assert data["data"]["first_name"] == "new@email.com"
    assert data["data"]["last_name"] == "new@email.com"

    response = client.post("/auth", headers={
        "Content-Type": "application/json",
        "App-Key": "xxlome",
        }, json={
            "username":"oldusername",
            "password":"newpassword"
        })
    assert response.status_code == 200, response.text
