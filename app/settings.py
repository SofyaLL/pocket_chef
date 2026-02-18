from functools import lru_cache
from pathlib import Path
from pydantic import SecretStr, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="allow")

    google_api_key: SecretStr = None
    model_name: str = "gemini-2.5-flash-lite"
    max_output_tokens: int = 10000

    mcp_url: HttpUrl = "http://localhost:9000/mcp"

    db_database: str = "postgres"
    DB_USER: str
    DB_PASSWORD: str
    db_port: int = 5432
    db_host: str = "localhost"


@lru_cache
def get_settings():
    return Settings()
