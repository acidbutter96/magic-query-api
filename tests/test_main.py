from fastapi.testclient import TestClient
from main import app
from utils.dotenv import config

client = TestClient(app)

def test_negative():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "application":"Magic Card Storage Application",
        "version": config['VERSION']
    }
