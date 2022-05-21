import pytest
from fastapi.testclient import TestClient
from main import app

from database.models.card import CardModel
from database.models.user import UserModel
from database.session import Base, get_db

from .database.session_db import TestingSessionLocal, engine

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

token = 'token'
def create_user():
    create_user = client.post(
        "/user/",
        json={
            "username":"oldusername",
            "email":"old@email.com",
            "first_name":"old",
            "last_name":"name",
            "password":"oldpassword",
        },
    )

    assert create_user.status_code == 200, create_user.text

def test_create_card():
    create_user()
    # Test if create route 
    request_body = {
            "card_name": "Card name one of magic",
            "edition": 1,
            "price": 150.1,
            "foil": True,
            "quantity": 1
        }

    response = client.post('/cards/create', headers={
        "Authorization": f"Bearer {token}",
        }, json=request_body)
    assert response.status_code == 200, response.text
    response = response.json()
    assert type(response["card_id"]) == int

    # Test if that was saved at database
    db = override_get_db()
    card = db.query(CardModel).filter(CardModel.id == response["card_id"]).first()
    assert card["card_name"] == request_body["card_name"]
    assert card["edition"] == request_body["edition"]
    assert card["price"] == request_body["price"]
    assert card["foil"] == request_body["foil"]
    assert card["quantity"] == request_body["quantity"]

def test_create_card_with_same_uid_name():
    create_user()
    db = override_get_db()
    request_body = {
            "card_name": "Card name one of magic",
            "edition": 2,
            "price": 150.1,
            "foil": True,
            "quantity": 5
        }

    response = client.post('/cards/create', headers={
        "Authorization": f"Bearer {token}",
        }, json=request_body)
    
    assert response.status_code == 200, response.text
    assert response["status"] == f"Card {request_body['card_name']} updated successfully"

    user_id = 1
    card = db.query(CardModel).filter(
        CardModel.id == user_id, CardModel.card_name == request_body['card_name']
    ).first()
    quantity:int = card["quantity"]
    assert quantity > request_body["quantity"], f"Expected: {quantity} > {request_body['quantity']}"
    # Test if the old attribute persists
    assert card["edition"] != request_body["edition"], f"{card['edition']} == {request_body['edition']}"
    assert card["price"] != request_body["price"], f"{card['edition']} == {request_body['edition']}"
    assert card["foil"] != request_body["foil"], f"{card['edition']} == {request_body['edition']}"    
    ...
