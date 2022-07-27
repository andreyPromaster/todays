import os
from unittest import mock

import pytest
from db.models.news import Base  # check if another Base exists
from db.models.utils import get_connection_engine
from sqlalchemy_utils import create_database, database_exists, drop_database


@pytest.fixture(scope="session")
def mock_db_creds():
    test_env = {
        **os.environ,
        "NEWS_DB_NAME": "test-db",
    }
    with mock.patch("os.environ", test_env):
        yield


@pytest.fixture
def setup_db(engine):
    if not database_exists(engine.url):
        create_database(engine.url)

    connection = engine.connect()
    Base.metadata.bind = connection
    Base.metadata.create_all()
    yield
    Base.metadata.drop_all()
    drop_database(engine.url)


@pytest.fixture(scope="session")
def engine(mock_db_creds):
    return get_connection_engine()


@pytest.fixture(scope="function")
def db_session(engine, setup_db, mock_db_creds):
    connection = engine.connect()

    transaction = connection.begin()
    yield
    transaction.rollback()
