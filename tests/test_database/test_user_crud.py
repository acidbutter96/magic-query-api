import pytest
from fastapi.testclient import TestClient
from main import app
from tests.test_database.database.database_testing_utils import get_token
from tests.test_database.database.session_db import TestingSessionLocal, engine

from database.models import UserModel, model_metadata
from database.session import Base, get_db

from .database.fake_database import fake_populated_user

# for meta in model_metadata:
#     meta.create_all(bind=engine)
#     ...

Base.metadata.create_all(bind=engine)
# def init_db():
#     db = TestingSessionLocal()

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def populate_database():
    db = TestingSessionLocal()
    db.query(UserModel).delete()
    db.commit()
    
    yield

    db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/user/",
        json={
            "username":"oldusername",
            "email":"old@email.com",
            "first_name":"old",
            "last_name":"name",
            "password":"oldpassword",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] == "User registered successfully", response.text

    # assert "id" in data, "aqui"
    # user_id = data["id"]
    # auth_data = get_token(client,"oldusername","oldpassword")

    # response = client.get(f"/user/", headers={
    #     "Authorization": f"Bearer {auth_data['token']}"
    #     })
    # assert response.status_code == 200, response.text
    # data = response.json()
    # assert data["username"] == "oldusername", "aquie"
    # assert data["first_name"] == "old"
    # assert data["last_name"] == "old"
    # assert data["email"] == "old@email.com"
    # assert data["id"] == user_id

def test_register_registered_user():
    response = client.post(
        "/user/",
        json={
            "username":"existentusername",
            "password":"password",
            "first_name":"Existent",
            "last_name":"User",
            "email":"existent@email.com",
        },
    )
    assert response.status_code == 200

    response = client.post(
        "/user/",
        json={
            "username":"existentusername",
            "password":"password2",
            "first_name":"Existent2",
            "last_name":"User2",
            "email":"existent2@email.com",
        },
    )

    assert response.status_code == 400

    data = response.json()
    assert data["detail"]["status"] == "User already exists", response.text

def test_register_registered_email():
    response = client.post(
        "/user/",
        json={
            "username":"existentemailusername",
            "password":"password",
            "first_name":"Existent Email",
            "last_name":"User",
            "email":"email@email.com",
        },
    )
    assert response.status_code == 200, response.text

    response = client.post(
        "/user/",
        json={
            "username":"username",
            "password":"password",
            "first_name":"Jane",
            "last_name":"Doe",
            "email":"email@email.com",
        },
    )

    data = response.json()
    assert data["detail"]["status"] == "The email is already registered, try another one"

def test_update_user():
    client.post(
        "/user/",
        json={
            "username":"oldusername",
            "password":"oldpassword",
            "first_name":"old",
            "last_name":"name",
            "email":"existent@email.com",
        },
    )

    data = get_token(client,"oldusername","oldpassword")

    response = client.put(
        "/user/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {data['token']}"
            }, json={
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

    assert "user" in data
    assert data["user"]["email"] == "new@email.com"
    assert data["user"]["first_name"] == "new@email.com"
    assert data["user"]["last_name"] == "new@email.com"

    response = client.post("/auth", headers={
        "Content-Type": "application/json",
        "App-Key": "xxlome",
        }, json={
            "username":"oldusername",
            "password":"newpassword"
        })
    assert response.status_code == 200, response.text

def test_delete_user():
    db = override_get_db() 
    data = get_token(client,"oldusername","oldpassword")

    response = client.delete(
        f"/user/",
        headers={'Authorization':f"Bearer {data['token']}"}
    )
    assert response.status_code == 200
    query = db.query(UserModel).filter(UserModel.id == data["id"]).first()
    assert query[0]["is_deleted"]
    response = client.get(f"/users/{data['id']}")
    assert response.status_code == 404

def test_delete_inexistent_user():
    """ 
        This test case is from the premise of the user executing the delete method twice with an active jwt  token.
    """
    db = override_get_db()
    data = get_token(client, "oldusername", "oldpassword")
    id = 1

    response1 = client.delete(f"/user/", headers={
        "Authorization": f"Bearer {data['token']}",
    })
    assert response1.status_code == 200
    assert response1.json()["info"] == f"user_id: {id} was deleted successfully."

    response2 = client.delete(f"")
    assert response2.status_code == 400
    assert response2.json()["detail"]["status"] == "There's no such user with the specified id, probably the user already was deleted."

    response3 = client.delete("/user/", headers={
        "Authorization": "Bearer falsebearertoken",
    })
    assert response3.status_code == 500
    assert response3.json()["detail"]["status"] == "User cannot be deleted"

def test_view_user():
    db = override_get_db()
    data = get_token(client, "oldusername", "oldpassword")
    request = client.get("/users/", headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {data['token']}"
        }
    )
    new_data = request.json()

    assert "id" in data
    assert new_data["id"] == data["id"]

    query = db.query(UserModel).filter(UserModel.id == data["id"]).first()

    assert new_data["id"] == query["id"]
    assert new_data["username"] == query["username"]
    assert new_data["email"] == query["email"]
    assert new_data["first_name"] == query["first_name"]
    assert new_data["last_name"] == query["last_name"]
