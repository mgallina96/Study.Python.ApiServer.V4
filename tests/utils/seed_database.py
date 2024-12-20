import asyncio

from faker import Faker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.models.main_postgres.customer import Customer
from system.databases.connections import get_database_engine
from system.databases.settings import DatabaseConnections
from system.logging.setup import init_logging


async def seed_customers(count: int) -> None:
    logger = await init_logging()

    engine = await get_database_engine(DatabaseConnections.MAIN_POSTGRES)
    async with AsyncSession(engine) as database_session:
        Faker.seed(0)
        fake = Faker()

        emails = set()
        for i in range(count):
            while (email := fake.email()) in emails:
                pass
            emails.add(email)
            customer = Customer(
                name=fake.name(),
                email=email,
                phone=fake.phone_number(),
                address=fake.address(),
            )
            database_session.add(customer)
            logger.info(f"Seeded customer {i + 1}/{count}: {customer}")
        await database_session.commit()


if __name__ == "__main__":
    asyncio.run(seed_customers(100_000))
