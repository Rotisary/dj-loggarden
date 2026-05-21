from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[4]

class Settings(BaseSettings):
    DATABASE_URL: str
    DEFAULT_LIMIT: int = 50
    MAX_LIMIT: int = 200

    model_config = SettingsConfigDict(
        env_prefix="LOGGARDEN_",
        env_file=BASE_DIR / ".env",
    )


settings = Settings()