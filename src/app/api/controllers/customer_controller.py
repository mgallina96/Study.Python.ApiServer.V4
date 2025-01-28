from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlmodel import select, Session

from app.api.schema.customer_schema import CustomerSchema, GetAllCustomersResponse
from app.api.schema.shared.base import CountMeta
from app.api.schema.shared.filtering import FilteringParams, get_filtering
from app.api.schema.shared.pagination import PaginationParams, get_pagination
from app.api.schema.shared.sorting import get_sorting, SortingParams
from app.core.models.main.customer import Customer
from system.database.session import DatabaseSession
from system.database.settings import DatabaseId

customer_router = APIRouter(prefix="/customers")


@customer_router.get("")
async def get_all(
    main_database_session: Session = Depends(DatabaseSession(DatabaseId.MAIN)),
    filtering: FilteringParams = Depends(get_filtering),
    sorting: SortingParams = Depends(get_sorting),
    pagination: PaginationParams = Depends(get_pagination(100, 300)),
) -> GetAllCustomersResponse:
    data_query = CustomerSchema.build_query(
        select(Customer),
        pagination.skip,
        pagination.limit,
        filtering.where,
        sorting.order_by,
    )
    data = main_database_session.exec(data_query).all()

    count_query = CustomerSchema.build_query(
        select(func.count(Customer.id)),
        where=filtering.where,
    )
    count = main_database_session.exec(count_query).one()

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
        meta=CountMeta(
            count=count,
        ),
    )
