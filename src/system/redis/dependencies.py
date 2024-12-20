from fastapi import Depends
from redis import asyncio as redis

from system.redis.models import RedisConnection
from system.redis.settings import RedisSettings
from system.settings.dependencies import get_settings


async def get_redis_settings() -> RedisSettings:
    return (get_settings()).redis


async def get_redis_connection(
    settings: RedisSettings = Depends(get_redis_settings),
) -> redis.Redis:
    async with RedisConnection(settings) as redis_connection:
        yield redis_connection
