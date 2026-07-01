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
    echo: bool = False
    pool_pre_ping: bool = True
    user: str
    password: str
    host: str
    port: int
    name: str

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env", env_prefix="DB_", extra="ignore"
    )

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def sync_url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class CORSSettings(BaseSettings):
    allowed_origins: list[str] = Field(alias="ALLOWED_ORIGINS")

    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", extra="ignore")


class ResendSettings(BaseSettings):
    RESEND_API_KEY: str
    FRONTEND_URL: str
    FROM_EMAIL: str
    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", extra="ignore")


class Settings(BaseSettings):
    resend: ResendSettings = ResendSettings()
    api: ApiSettings = ApiSettings()
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    cors: CORSSettings = CORSSettings()
    encoding: str = "utf-8"


settings = Settings()
