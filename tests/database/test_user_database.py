from fastapi.testclient import TestClient
from main import app
from tests.database.database_testing_utils import get_token
from tests.database.session_test_db import TestingSessionLocal, engine

from database.models import UserModel, model_metadata
from database.session import Base, get_db

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

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users/",
        json={
            "username":"oldusername",
            "email":"old@email.com",
            "first_name":"old",
            "last_name":"name",
            "password":"oldpassword",
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["status"] == "User registered successfully"

    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "oldusername"
    assert data["first_name"] == "old"
    assert data["last_name"] == "old"
    assert data["email"] == "old@email.com"
    assert data["id"] == user_id

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
    assert response.status_code == 400

    data = response.json()
    assert data["status"] == "User already exists"

def test_register_registered_email():
    response = client.post(
        "/users/",
        json={
            "username":"existentemailusername",
            "password":"password",
            "first_name":"Existent Email",
            "last_name":"User",
            "email":"email@email.com",
        },
    )
    assert response.status_code == 409

    data = response.json()
    assert data["status"] == "The email is already registered, try another one"

def test_update_user():
    data = get_token(client,"oldusername","oldpassword")

    response = client.put(
        "/users/",
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
