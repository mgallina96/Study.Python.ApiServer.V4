from fastapi import APIRouter, Depends

from app.api.schema.shared.filtering import FilteringParams, get_filtering
from app.api.schema.shared.pagination import PaginationParams, get_pagination
from app.api.schema.shared.sorting import get_sorting, SortingParams
from system.query_builder.rules import And, Equal, LessThanOrEqual

customer_router = APIRouter(prefix="/customers")


@customer_router.get("")
async def get_customers(
    filtering: FilteringParams = Depends(get_filtering),
    sorting: SortingParams = Depends(get_sorting),
    pagination: PaginationParams = Depends(get_pagination(100, 300)),
):
    where = And(
        rules=[
            Equal(field="name", value="pippo"),
            LessThanOrEqual(field="age", value=30),
        ]
    )
    return {
        "pagination": pagination,
        "filtering": filtering,
        "sorting": sorting,
        "test_where": where,
    }
