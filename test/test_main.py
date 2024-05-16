from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_check_healthy() -> None:
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "I am healthy!"}
