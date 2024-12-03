import redis

from system.datetime.settings import DatetimeSettings
from system.logging.settings import LoggingSettings
from system.redis.models import RedisConnection
from system.redis.settings import RedisSettings
from system.settings.models import (
    Settings,
    StartupSettings,
)

_settings: Settings | None = None


class SettingsNotLoadedError(Exception):
    pass


async def get_settings() -> Settings:
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

    global _settings
    if _settings is None:
        # noinspection PyArgumentList
        startup_settings = StartupSettings()
        settings_prefix = f"settings:{startup_settings.app_name}:"

        try:
            async with RedisConnection(
                startup_settings.redis_startup
            ) as redis_connection:
                _, keys = await redis_connection.scan(
                    match=f"{settings_prefix}*", count=1_000
                )
                values = await redis_connection.mget(keys)
        except redis.exceptions.ConnectionError as exc:
            raise SettingsNotLoadedError(
                "Could not connect to Redis for settings"
            ) from exc

        settings_dict = unflatten_tree(
            keys, values, separator=":", prefix=settings_prefix
        )
        _settings = Settings(**settings_dict)

    return _settings


async def get_redis_settings() -> RedisSettings:
    return (await get_settings()).redis


async def get_logging_settings() -> LoggingSettings:
    return (await get_settings()).logging


async def get_datetime_settings() -> DatetimeSettings:
    return (await get_settings()).datetime
