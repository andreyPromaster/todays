from tests.factories import ThemeFactory
from tests.utils import client


def test_get_theme(db_session):
    theme = ThemeFactory(db_session)()
    response = client.get(f"/themes/{theme.id}")
    assert response.status_code == 200
