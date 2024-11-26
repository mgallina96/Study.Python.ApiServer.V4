from functools import lru_cache

import redis
from pydantic import BaseModel, SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings


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


@lru_cache
def get_settings() -> Settings:
    def unflatten_tree(
        _keys: list[bytes],
        _values: list[bytes],
        *,
        separator: str,
        prefix: str,
    ) -> dict:
        tree = {}
        for key, value in zip(_keys, _values):
            parts = key.decode().removeprefix(prefix).split(separator)
            current = tree
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = value.decode()
        return tree

    # noinspection PyArgumentList
    startup_settings = StartupSettings()
    settings_prefix = f"settings:{startup_settings.instance_name}:"
    with redis.Redis(
        host=startup_settings.config_redis.host,
        port=startup_settings.config_redis.port,
        db=startup_settings.config_redis.db,
        username=startup_settings.config_redis.username,
        password=(
            startup_settings.config_redis.password.get_secret_value()
            if startup_settings.config_redis.password
            else None
        ),
    ) as redis_connection:
        keys = list(redis_connection.scan_iter(match=f"{settings_prefix}*"))
        values = redis_connection.mget(keys)

    settings_dict = unflatten_tree(keys, values, separator=":", prefix=settings_prefix)
    settings = Settings(**settings_dict)
    return settings
