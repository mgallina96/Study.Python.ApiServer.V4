from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseModel):
    host: str
    port: int
    db: int
    username: str | None = None
    password: SecretStr | None = None


class DatabaseSettings(BaseModel):
    sync_connection_string: str
    async_connection_string: str
    password: SecretStr
    pool_size: int


class StartupSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
    )

    instance_name: str
    config_redis: RedisSettings


class Settings(StartupSettings):
    redis: RedisSettings
