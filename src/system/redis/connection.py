import redis
from fastapi import Depends

from system.redis.settings import RedisSettings
from system.settings import get_redis_settings


def get_redis_connection(
    settings: RedisSettings = Depends(get_redis_settings),
) -> redis.Redis:
    with redis.Redis(
        protocol=3,
        host=settings.host,
        port=settings.port,
        db=settings.db,
        username=settings.username,
        password=(settings.password.get_secret_value() if settings.password else None),
    ) as redis_connection:
        yield redis_connection
