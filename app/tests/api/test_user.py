from factories import UserFactory
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_user_registration(db_session):
    breakpoint()
    user = UserFactory()
    print(user)
    response = client.post(
        "/register/",
        json={
            "email": "User-test-0@mail.com",
            "password": "12sdfa!EF3",
            "second_password": "12sdfa!EF3",
        },
    )
    assert response.status_code == 200
