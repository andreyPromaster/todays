from tests.factories import ThemeFactory
from tests.utils import client


def test_get_theme(db_session):
    theme = ThemeFactory()
    response = client.get(f"/theme/{theme.id}")
    assert response.status_code == 201
