import os
from unittest import mock

import pytest
from db.models.news import Base  # check if another Base exists
from db.models.utils import get_connection_engine
from sqlalchemy.orm import Session


@pytest.fixture(scope="session")
def mock_db_creds():
    test_env = {
        **os.environ,
        "DB_NAME": "test",
        "DB_HOST": "127.0.0.1",
        "DB_PORT": "9999",
        "DB_PASS": "testing_password",
        "DB_USER": "testing",
    }
    with mock.patch("os.environ", test_env):
        yield


@pytest.fixture
def setup_db(engine):
    connection = engine.connect()
    Base.metadata.bind = connection
    Base.metadata.create_all()
    yield
    Base.metadata.drop_all()


@pytest.fixture(scope="session")
def engine(mock_db_creds):
    return get_connection_engine()


@pytest.fixture(scope="function")
def db_session(engine, setup_db):
    connection = engine.connect()

    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
