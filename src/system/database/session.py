from sqlalchemy import Engine
from sqlmodel import create_engine, Session

from system.database.settings import (
    DatabaseId,
    DatabaseSettings,
)
from system.settings import get_database_settings

database_engines: dict[DatabaseId, Engine] = {}

main_database_settings: DatabaseSettings = get_database_settings(DatabaseId.MAIN)
database_engines[DatabaseId.MAIN] = create_engine(
    main_database_settings.connection_string.format(
        password=main_database_settings.password.get_secret_value()
    ),
    pool_size=main_database_settings.pool_size,
    pool_pre_ping=True,
    echo=True,
    echo_pool=True,
)


class DatabaseSession:
    database_id: DatabaseId

    def __init__(self, database_id: DatabaseId):
        self.database_id = database_id

    def __call__(self) -> Session:
        engine = database_engines[self.database_id]
        with Session(engine) as database_session:
            yield database_session
