from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

client = TestClient(app)


def test_get_all_user() -> None:
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
