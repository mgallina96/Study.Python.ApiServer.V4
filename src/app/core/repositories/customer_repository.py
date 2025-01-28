from app.core.models.main.customer import Customer
from app.core.repositories._base import BaseRepository
from system.query_builder.rules import Field


class CustomerRepository(BaseRepository):
    def __init__(self):
        super().__init__(
            query_builder_fields=[
                Field("id", Customer.id),
                Field("email", Customer.email),
            ]
        )
