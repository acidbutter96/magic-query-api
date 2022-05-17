from fastapi.testclient import TestClient
from main import app

testclient = TestClient(app)

def test_negative():
    assert 1==2
