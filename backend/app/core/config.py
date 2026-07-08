from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_DB_URL = (
    f"sqlite+aiosqlite:///{Path(__file__).resolve().parents[2] / 'hireflow.db'}"
)
TEST_DB_URL = (
    f"sqlite+aiosqlite:///{Path(__file__).resolve().parents[2] / 'test_hireflow.db'}"
)


class Settings(BaseSettings):
    testing: bool = False
    database_url: str | None = None
    cors_origins: list[str] = ["http://localhost:3000"]
    # Default matches .env.example; override via AI_MODEL when deploying.
    ai_model: str = "anthropic:claude-sonnet-4-6"

    @model_validator(mode="after")
    def set_default_database_url(self) -> "Settings":
        if self.testing:
            self.database_url = TEST_DB_URL
            return self

        if self.database_url:
            return self

        self.database_url = DEFAULT_DB_URL
        return self

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

if __name__ == "__main__":
    # uv run backend/app/core/config.py
    print(settings.ai_model)
