from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.environ import EnvManager


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    """
    Класс конфигурации приложения FastAPI

    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    DOMAIN: str = "localhost:8000"
    ENVIRONMENT: Literal["local", "test", "staging", "production"] = "local"
    BASE_PATH: Path = Path(__file__).resolve().parent.parent.parent
    APP_DIR: Path = BASE_PATH / "src"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def server_host(self) -> str:
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str,
        BeforeValidator(parse_cors),
    ] = []
    PROJECT_NAME: str = "task-manager"
    SENTRY_DSN: HttpUrl | None = None
    DB_HOST: str = EnvManager.get_str("DB_HOST", default="localhost")
    DB_PORT: int = 5432
    DB_LOGIN: str = EnvManager.get_str("DB_LOGIN", default="postgres")
    DB_PASSWORD: str = EnvManager.get_str("DB_PASSWORD", default="qrymirald5186")
    DB_NAME: str = EnvManager.get_str("DB_NAME", default="postgres")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return str(
            MultiHostUrl.build(
                scheme="postgresql+asyncpg",
                username=self.DB_LOGIN,
                password=self.DB_PASSWORD,
                host=self.DB_HOST,
                port=self.DB_PORT,
                path=self.DB_NAME,
            ),
        )


settings = Settings()  # type: ignore
