from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.constants import BACKEND_DIR


class ApiSettings(BaseSettings):
    API_KEY: str

    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", extra="ignore")

class RedisSettings(BaseSettings):
    url: str = Field(alias="REDIS_URL")
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env", populate_by_name=True, extra="ignore"
    )

class DatabaseSettings(BaseSettings):
    user: str
    password: str
    host: str
    port: int
    name: str

    model_config = SettingsConfigDict(env_prefix='DB_')

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    api: ApiSettings = ApiSettings()
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    encoding: str = "utf-8"


settings = Settings()
