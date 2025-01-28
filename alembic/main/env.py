from alembic import context

from system.database.session import database_engines
from system.database.settings import DatabaseId


engine = database_engines[DatabaseId.MAIN]
with engine.connect() as connection:
    context.configure(connection=connection)
    with context.begin_transaction():
        context.run_migrations()
