import pytest
from fastapi.testclient import TestClient
from main import app

from models.user import UserModel

client = TestClient(app)

def test_users_not_allowed():
    response = client.get("/users/", headers={
        "Content-Type": "application/json",
        })
    
    assert response.status_code != 401
    assert response.json() != {
        "user": {
            "first_name": "",
            "last_name": "",
            "username": "",
            "created_at": "",
            "updated_at": ""
        }
    }

def test_login_authentication():
    response = client.post("/auth",headers={
        "app-key":"xxlome",
        "Content-Type": "application/json"
        },
        json={
        "username":"acidbutter",
        "password":"123456"})

    assert response.status_code == 200
    assert response.json() == {
        # "access_token": user.username,
        "token_type": "bearer"
    }
