from pydantic import field_serializer

from app.api.schema.shared.base import CountMeta, BaseSchema
from system.id_obfuscation.dependencies import get_id_obfuscator_factory
from system.query_builder.rules import WhereRule, OrderByRule


class CustomerSchema(BaseSchema):
    id: int
    name: str
    email: str
    phone: str
    address: str

    @field_serializer("id")
    def obfuscate_id(self, value: int) -> str | None:
        if value is None:
            return None
        return (
            get_id_obfuscator_factory()
            .get_obfuscator(self.__class__.__name__)
            .encode(value)
        )


class GetAllCustomersResponse(BaseSchema):
    class Meta(CountMeta):
        skip: int
        limit: int
        where: WhereRule | None
        order_by: list[OrderByRule] | None

    data: list[CustomerSchema]
    meta: Meta
