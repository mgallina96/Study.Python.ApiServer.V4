import redis.asyncio as redis
from fastapi import Depends

from system.settings.models import RedisSettings


class RedisConnection:
    _redis: redis.Redis | None
    _settings: RedisSettings

    def __init__(self, settings: RedisSettings):
        self._redis = None
        self._settings = settings

    async def __aenter__(self) -> redis.Redis:
        self._redis = redis.Redis(
            protocol=3,
            host=self._settings.host,
            port=self._settings.port,
            db=self._settings.db,
            username=self._settings.username,
            password=(
                self._settings.password.get_secret_value()
                if self._settings.password
                else None
            ),
        )
        return self._redis

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._redis.aclose()


async def get_redis_connection(settings: RedisSettings = Depends()) -> redis.Redis:
    async with RedisConnection(settings) as redis_connection:
        yield redis_connection
