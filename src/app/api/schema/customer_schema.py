from app.api.schema.shared.base import CountMeta, BaseSchema, BaseEntitySchema
from app.core.models.main.customer import Customer
from system.query_builder.rules import Field


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
