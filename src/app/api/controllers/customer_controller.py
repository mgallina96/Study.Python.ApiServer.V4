from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.schema.customer_schema import CustomerSchema, GetAllCustomersResponse
from app.api.schema.shared.filtering import FilteringParams, get_filtering
from app.api.schema.shared.pagination import PaginationParams, get_pagination
from app.api.schema.shared.sorting import get_sorting, SortingParams
from app.core.models.main_postgres.customer import Customer
from system.databases.dependencies import get_main_postgres

customer_router = APIRouter(prefix="/customers")


@customer_router.get("")
async def get_all(
    main_postgres: AsyncSession = Depends(get_main_postgres),
    filtering: FilteringParams = Depends(get_filtering),
    sorting: SortingParams = Depends(get_sorting),
    pagination: PaginationParams = Depends(get_pagination(100, 300)),
) -> GetAllCustomersResponse:
    base_query = select(Customer)
    if filtering.where:
        base_query = base_query.where(filtering.where.compile())

    query = base_query.offset(pagination.skip).limit(pagination.limit)
    result = await main_postgres.exec(query)
    data = result.all()

    count_query = select(func.count(Customer.id))
    count_result = await main_postgres.exec(count_query)
    count = count_result.one()

    return GetAllCustomersResponse(
        data=[
            CustomerSchema(
                id=d.id,
                name=d.name,
                email=d.email,
                phone=d.phone,
                address=d.address,
            )
            for d in data
        ],
        meta=GetAllCustomersResponse.Meta(
            count=count,
            skip=pagination.skip,
            limit=pagination.limit,
            where=filtering.where,
            order_by=sorting.order_by,
        ),
    )
