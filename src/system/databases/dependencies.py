from sqlmodel.ext.asyncio.session import AsyncSession

from system.databases.connections import get_database_engine
from system.databases.settings import DatabaseConnections


async def get_main_postgres() -> AsyncSession:
    engine = get_database_engine(DatabaseConnections.MAIN_POSTGRES)
    async with AsyncSession(engine) as database_session:
        yield database_session
