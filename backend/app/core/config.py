from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="DISTROHUB_",
        extra="ignore",
    )

    app_name: str = "DistroHub"
    app_version: str = "0.1.0"
    environment: Literal["development", "testing", "production"] = "development"
    debug: bool = False
    docker_host: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
