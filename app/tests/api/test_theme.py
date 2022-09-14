import pytest
from db.models.news import Theme
from tests.factories import ThemeFactory
from tests.utils import client


def test_get_theme(db_session):
    theme = ThemeFactory(db_session).create()
    response = client.get(f"/themes/{theme.id}")
    assert response.status_code == 200


@pytest.mark.parametrize("count", [0, 5, 10])
def test_get_themes(db_session, count):
    ThemeFactory(db_session).create_batch(count)
    response = client.get("/themes/")
    assert response.status_code == 200
    assert len(response.json()) == count


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


def test_update_theme(db_session):
    theme = ThemeFactory(db_session).create()
    update_name = "New name"
    response = client.put(f"/themes/{theme.id}", json={"name": update_name})

    db_session.expunge_all()
    expected_theme = db_session.query(Theme).first()

    assert response.status_code == 200
    assert expected_theme.name == update_name
    assert expected_theme.description == theme.description
