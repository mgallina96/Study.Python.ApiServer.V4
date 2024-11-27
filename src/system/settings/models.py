from typing import Type, Tuple

from pydantic import BaseModel, SecretStr, Json
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
)


class RedisSettings(BaseModel):
    host: str
    port: int
    db: int
    username: str | None = None
    password: SecretStr | None = None


class StartupSettings(BaseSettings):
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return env_settings, dotenv_settings, init_settings, file_secret_settings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
    )

    app_name: str
    redis_startup: RedisSettings


class DatabaseSettings(BaseModel):
    sync_connection_string: str
    async_connection_string: str
    password: SecretStr
    pool_size: int


class LoggingSinkSettings(BaseModel):
    enabled: bool
    format: str
    root_level: str


class LoggingSinkFileSettings(LoggingSinkSettings):
    path: str
    backup_count: int


class LoggingSettings(BaseModel):
    root_level: str
    console: LoggingSinkSettings
    file: LoggingSinkFileSettings
    module_levels: Json[dict[str, str]]


class Settings(StartupSettings):
    redis: RedisSettings
    logging: LoggingSettings
