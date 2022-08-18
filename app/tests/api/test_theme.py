from tests.factories import ThemeFactory
from tests.utils import client


def test_create_theme(db_session):
    #  user = UserFactory()
    response = client.post(
        "/themes/",
        json={
            "name": f"{ThemeFactory.name}",
            "description": ThemeFactory.description,
        },
    )
    breakpoint()
    assert response.status_code == 200
