import os
from functools import lru_cache

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):

    DB_USERNAME: str = os.environ.get("DB_USERNAME", "")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "")
    DB_HOST: str = os.environ.get("DB_HOST", "localhost")
    DB_PORT: int = os.environ.get("DB_PORT", 5434)
    DB_NAME: str = os.environ.get("DB_NAME", "")

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")
    ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")

    REDIS_HOST: str = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT: int = os.environ.get("REDIS_PORT", 6379)

    class Config:
        env_file = ".env"


@lru_cache()
def get_config():
    return Settings()

config = get_config()