from functools import lru_cache
from pathlib import Path
from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    google_api_key: SecretStr = None
    model_name: str
    
    max_output_tokens: int = 10000 
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="allow")


@lru_cache
def get_settings():
    return Settings()