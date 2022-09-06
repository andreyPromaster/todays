import contextlib

import pytest
from api.dependencies import get_db
from db.models.news import Base  # check if another Base exists
from main import app
from sqlalchemy_utils import create_database, database_exists, drop_database
from utils import TestingSessionLocal, engine, override_get_db


@pytest.fixture(scope="session")
def setup_db():
    if not database_exists(engine.url):
        create_database(engine.url)

    connection = engine.connect()
    Base.metadata.bind = connection
    Base.metadata.create_all()
    yield connection
    Base.metadata.drop_all()
    connection.close()
    drop_database(engine.url)


@pytest.fixture()
def db_session(setup_db):
    session = TestingSessionLocal(bind=setup_db)
    app.dependency_overrides[get_db] = override_get_db
    yield session
    session.rollback()
    # Cleanup database
    with contextlib.closing(engine.connect()) as connection:
        transaction = connection.begin()
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())
        transaction.commit()
