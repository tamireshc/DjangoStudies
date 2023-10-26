from typing import ClassVar

from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://root:1234567@localhost:5432/faculdade3"
    DBBaseModel: ClassVar = declarative_base()

    JWT_SECRET: str = "super_secreto"
    ALGORITHM: str = "HS256"
    ACESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings = Settings()
