from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.constants import BACKEND_DIR


class ApiSettings(BaseSettings):
    API_KEY: str

    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", extra="ignore")


class DatabaseSettings(BaseSettings):
    url: str = Field(alias="DATABASE_URL")
    echo: bool = False
    pool_pre_ping: bool = True
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env", populate_by_name=True, extra="ignore"
    )


class Settings(BaseSettings):
    api: ApiSettings = ApiSettings()
    db: DatabaseSettings = DatabaseSettings()
    encoding: str = "utf-8"


settings = Settings()
