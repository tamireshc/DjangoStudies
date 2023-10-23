from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://root:1234567@localhost:5432/faculdade2"

    class Config:
        case_sensitive = True


settings = Settings()
