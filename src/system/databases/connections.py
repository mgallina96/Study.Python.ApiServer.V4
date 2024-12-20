import logging
from logging import Logger

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from system.databases.settings import DatabaseConnections
from system.settings.dependencies import get_settings
from system.settings.models import Settings

logger: Logger = logging.getLogger(__name__)

_database_connections: dict[DatabaseConnections, AsyncEngine] = {}


def init_database_engines(settings: Settings = None) -> None:
    global _database_connections

    settings = settings or get_settings()

    _database_connections = {
        DatabaseConnections.MAIN_POSTGRES: create_async_engine(
            settings.databases.main_postgres.connection_string.format(
                password=settings.databases.main_postgres.password.get_secret_value(),
            ),
            pool_pre_ping=True,
            pool_size=settings.databases.main_postgres.pool_size,
        ),
    }


def get_database_engine(connection: DatabaseConnections) -> AsyncEngine:
    if not _database_connections:
        init_database_engines()
    return _database_connections[connection]
