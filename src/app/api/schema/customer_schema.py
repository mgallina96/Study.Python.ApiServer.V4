from app.api.schema.shared.base import CountMeta, BaseSchema, BaseEntitySchema
from system.query_builder.rules import WhereRule, OrderByRule


class CustomerSchema(BaseEntitySchema):
    name: str
    email: str
    phone: str
    address: str


class GetAllCustomersResponse(BaseSchema):
    class Meta(CountMeta):
        skip: int
        limit: int
        where: WhereRule | None
        order_by: list[OrderByRule] | None

    data: list[CustomerSchema]
    meta: Meta
