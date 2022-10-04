from db.models.utils import configurate_database_connection_string
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(configurate_database_connection_string(NEWS_DB_NAME="test"))
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


def override_get_db(session=None):
    try:
        db = TestingSessionLocal() if session is None else session
        yield db
    finally:
        db.close()
