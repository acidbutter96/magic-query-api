from fastapi.testclient import TestClient
from main import app

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

def test_create_card():
    response = client.post('/cards/create', )
