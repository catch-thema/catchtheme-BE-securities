from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str
    USE_MOCK_DATA: bool

    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()