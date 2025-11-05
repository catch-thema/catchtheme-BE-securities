from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str
    USE_MOCK_DATA: bool

    DATABASE_URL: str

    KIS_APP_KEY: str = ""
    KIS_APP_SECRET: str = ""
    KIS_BASE_URL: str = ""

    KOREAEXIM_API_KEY: str = ""
    KOREAEXIM_BASE_URL: str = ""

    class Config:
        env_file = ".env"

settings = Settings()