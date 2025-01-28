import asyncio

from faker import Faker
from sqlmodel import Session
from uuid6 import uuid7

from app.core.models.main.customer import Customer
from system.database.session import database_engines
from system.database.settings import DatabaseId
from system.logging.setup import init_logging


async def seed_customers(count: int) -> None:
    logger = init_logging()

    engine = database_engines[DatabaseId.MAIN]
    with Session(engine) as database_session:
        fake = Faker()

        for i in range(count):
            customer_id = uuid7()
            customer = Customer(
                id=customer_id,
                name=fake.name(),
                email=f"{customer_id}@{fake.free_email_domain()}",
                phone=fake.phone_number(),
                address=fake.address(),
            )
            database_session.add(customer)
            logger.info(f"Seeded customer {i + 1}/{count}: {customer}")
        database_session.commit()


if __name__ == "__main__":
    total_count = 10_000
    batch_size = 10_000
    for _ in range(total_count // batch_size):
        asyncio.run(seed_customers(batch_size))
