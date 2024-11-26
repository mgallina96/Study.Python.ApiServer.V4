import redis

_redis_connection_pool: redis.ConnectionPool | None = None


def get_redis_connection() -> redis.Redis:
    global _redis_connection_pool
    if _redis_connection_pool is None:
        _redis_connection_pool = redis.ConnectionPool()
    return redis.Redis(connection_pool=_redis_connection_pool)
