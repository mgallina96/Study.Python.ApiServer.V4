from typing import Type, Tuple

from pydantic import BaseModel, SecretStr
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
)

from system.datetime.settings import DatetimeSettings
from system.logging.settings import LoggingSettings
from system.redis.settings import RedisSettings


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


class Settings(StartupSettings):
    redis: RedisSettings
    logging: LoggingSettings
    datetime: DatetimeSettings
