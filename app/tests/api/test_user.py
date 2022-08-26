from factories import UserFactory
from utils import client


def test_success_user_registration(db_session):
    fake_user = UserFactory.build(email="User-test@mail.com", password="12sdfa!EF3")
    response = client.post(
        "/register/",
        json={
            "email": fake_user.email,
            "password": fake_user.password,
            "second_password": fake_user.password,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["email"] == fake_user.email
    assert payload["id"] is not None
    assert "image" in payload.keys()


def test_not_the_same_password_user_registration(db_session):
    fake_user = UserFactory.build(email="User-test@mail.com", password="12sdfa!EF3")
    response = client.post(
        "/register/",
        json={
            "email": fake_user.email,
            "password": fake_user.password,
            "second_password": f"wrong-{fake_user.password}",
        },
    )
    assert response.status_code == 422
    payload = response.json()
    assert "second_password" in payload["detail"][0]["loc"]
    assert payload["detail"][0]["msg"] == "Passwords do not match"


def test_registration_user_already_exists(db_session):
    fake_user = UserFactory(email="User-test@mail.com", password="12sdfa!EF3")
    response = client.post(
        "/register/",
        json={
            "email": fake_user.email,
            "password": fake_user.password,
            "second_password": fake_user.password,
        },
    )
    assert response.status_code == 401
    payload = response.json()
    assert payload["detail"] == "Incorrect email or password"
