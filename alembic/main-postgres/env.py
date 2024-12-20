import asyncio

from alembic import context

from system.databases.connections import get_database_engine
from system.databases.settings import DatabaseConnections
from system.logging.setup import init_logging


async def run_migrations_online() -> None:
    def run_migrations(_connection):
        context.configure(connection=_connection)

        with context.begin_transaction():
            context.run_migrations()

    await init_logging()
    engine = await get_database_engine(DatabaseConnections.MAIN_POSTGRES)
    async with engine.connect() as connection:
        await connection.run_sync(run_migrations)


asyncio.run(run_migrations_online())
