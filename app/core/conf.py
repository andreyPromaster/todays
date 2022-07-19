from pydantic import BaseSettings


class PostgreSQLSettings(BaseSettings):
    NEWS_DB_USER: str = "postgres"
    NEWS_DB_HOST: str = ""
    NEWS_DB_PORT: int = 5432
    NEWS_DB_NAME: str = "todays"
    NEWS_DB_PASSWORD: str = ""


SECRET_KEY = "22d17264220bb02422b21f512525677b11c1eb82c260b8d8d3f4485cca68c0e8"
TOKEN_ENCRYPTION_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
