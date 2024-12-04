from sqlalchemy import Select

from system.query_builder.rules import (
    _Conditions,
    _BaseOrderByRule,
    _EngineContext,
    Field,
)
from system.query_builder.rules import WhereRule


def join_where_rules(
    *where: WhereRule | None, condition: _Conditions = _Conditions.AND
) -> WhereRule | None:
    rules = [rule for rule in where if rule is not None]
    if not rules:
        return None
    return WhereRule(rules=rules, condition=condition)


def build_query(
    fields: list[Field],
    base_query: Select,
    skip: int | None = None,
    limit: int | None = None,
    where: WhereRule | None = None,
    order_by: list[_BaseOrderByRule] | None = None,
) -> Select:
    engine_context = _EngineContext(fields)

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
