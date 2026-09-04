from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "development"
    log_level: str = "INFO"
    api_v1_prefix: str = "/api/v1"
    frontend_url: str = "http://localhost:3000"
    database_url: str | None = Field(default=None)
    max_upload_size_mb: int = Field(default=25, ge=1, le=1024)
    upload_dir: Path = Path("storage/uploads")

    @field_validator("database_url", mode="before")
    @classmethod
    def empty_database_url(cls, value: object) -> object:
        if value == "":
            return None
        return value

    @property
    def is_development(self) -> bool:
        return self.environment.lower() in {"development", "dev", "local"}

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.frontend_url.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
