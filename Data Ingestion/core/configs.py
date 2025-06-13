from pydantic.v1 import BaseSettings
from sqlalchemy.orm import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "sqlite+aiosqlite:///db.sqlite3"
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = False
        env_file = ".env"

settings = Settings()