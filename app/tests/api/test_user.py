#  from factories import UserFactory
from utils import client


def test_user_registration(db_session):
    #  user = UserFactory()
    response = client.post(
        "/register/",
        json={
            "email": "User-test-1@mail.com",
            "password": "12sdfa!EF3",
            "second_password": "12sdfa!EF3",
        },
    )
    assert response.status_code == 200
