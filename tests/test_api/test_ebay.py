from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ebay():
    response_mario_montreal = client.get("/ebay/?user_search=mario&user_location=Montreal")
    assert response_mario_montreal.status_code == 200
    assert response_mario_montreal.json() == {"ads": ["ABC"]}
