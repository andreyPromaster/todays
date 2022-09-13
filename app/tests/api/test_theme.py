import pytest
from db.models.news import Theme
from tests.factories import ThemeFactory
from tests.utils import client


def test_get_theme(db_session):
    theme = ThemeFactory(db_session).create()
    response = client.get(f"/themes/{theme.id}")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "data,expected_value",
    [
        ({"name": "New Theme"}, None),
        ({"name": "Any new Theme", "description": "some description"}, "some description"),
    ],
)
def test_create_new_theme(db_session, data, expected_value):
    theme = data
    response = client.post(
        "/themes/", json={"name": theme["name"], "description": theme.get("description")}
    )
    expected_theme = db_session.query(Theme).first()
    assert response.status_code == 200
    assert expected_theme.name == theme["name"]
    assert expected_theme.description == expected_value
