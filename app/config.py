from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent


class RunConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000


class DatabaseSettings(BaseSettings):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class AccessToken(BaseSettings):
    expires_delta: timedelta = timedelta(hours=2)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra='ignore'
    )

    run: RunConfig = RunConfig()
    access_token: AccessToken = AccessToken()
    database: DatabaseSettings


settings = Settings() # type: ignore
