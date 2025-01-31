from app.api.schema.shared.base import CountMeta, BaseSchema
from app.api.schema.shared.entities import BaseEntitySchema
from app.core.models.main.customer import Customer
from system.query_builder import Field


class CustomerSchema(BaseEntitySchema):
    name: str
    email: str
    phone: str
    address: str

    @staticmethod
    def get_query_builder_fields() -> list[Field]:
        return [
            Field("id", Customer.id),
            Field("email", Customer.email),
        ]


class GetAllCustomersResponse(BaseSchema):
    data: list[CustomerSchema]
    meta: CountMeta


class GetCustomerResponse(BaseSchema):
    data: CustomerSchema
