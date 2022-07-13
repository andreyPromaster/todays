from pydantic import BaseSettings


class PostgreSQLSettings(BaseSettings):
    NEWS_DB_USER: str = "postgres"
    NEWS_DB_HOST: str = ""
    NEWS_DB_PORT: int = 5432
    NEWS_DB_NAME: str = "todays"
    NEWS_DB_PASSWORD: str = ""
