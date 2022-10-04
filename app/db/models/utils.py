import json
from functools import partial

from core.conf import PostgreSQLSettings
from pydantic.json import pydantic_encoder
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_connection_engine() -> Engine:
    conn = create_engine(
        configurate_database_connection_string(),
        json_serializer=partial(json.dumps, default=pydantic_encoder),
        echo=True,
    )
    return conn


def configurate_database_connection_string(**kwargs) -> str:
    setting = PostgreSQLSettings(**kwargs)
    return (
        f"postgresql://{setting.NEWS_DB_USER}:{setting.NEWS_DB_PASSWORD}"
        f"@{setting.NEWS_DB_HOST}:{setting.NEWS_DB_PORT}/{setting.NEWS_DB_NAME}"
    )
