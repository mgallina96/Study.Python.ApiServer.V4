from functools import lru_cache

from system.redis import RedisConnection
from system.settings.models import Settings, StartupSettings


@lru_cache
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

    # noinspection PyArgumentList
    startup_settings = StartupSettings()
    settings_prefix = f"settings:{startup_settings.instance_name}:"

    async with RedisConnection(startup_settings.config_redis) as redis_connection:
        _, keys = await redis_connection.scan(match=f"{settings_prefix}*")
        values = await redis_connection.mget(keys)

    settings_dict = unflatten_tree(keys, values, separator=":", prefix=settings_prefix)
    settings = Settings(**settings_dict)
    return settings
