from abc import ABC

from sqlalchemy import Select

from system.query_builder.rules import Field, WhereRule, OrderByRule, EngineContext


class BaseRepository(ABC):
    query_builder_fields: list[Field]

    def __init__(self, query_builder_fields: list[Field]):
        self.query_builder_fields = query_builder_fields

    def build_query(
        self,
        base_query: Select,
        skip: int | None = None,
        limit: int | None = None,
        where: WhereRule | None = None,
        order_by: list[OrderByRule] | None = None,
    ) -> Select:
        engine_context = EngineContext(self.query_builder_fields)

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
