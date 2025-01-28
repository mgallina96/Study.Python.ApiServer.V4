from abc import abstractmethod
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import Select

from system.query_builder.rules import Field, WhereRule, OrderByRule, EngineContext


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class BaseEntitySchema(BaseSchema):
    id: UUID

    @staticmethod
    @abstractmethod
    def get_query_builder_fields() -> list[Field]:
        raise NotImplementedError()

    @classmethod
    def build_query(
        cls,
        base_query: Select,
        skip: int | None = None,
        limit: int | None = None,
        where: WhereRule | None = None,
        order_by: list[OrderByRule] | None = None,
    ) -> Select:
        engine_context = EngineContext(cls.get_query_builder_fields())

        if skip:
            base_query = base_query.offset(skip)
        if limit:
            base_query = base_query.limit(limit)
        if where:
            compiled_where = where.compile(engine_context)
            base_query = base_query.where(compiled_where)
        if order_by:
            compiled_order_by = [rule.compile(engine_context) for rule in order_by]
            base_query = base_query.order_by(*compiled_order_by)

        base_query = base_query.params(engine_context.params)

        return base_query


class CountMeta(BaseSchema):
    count: int
