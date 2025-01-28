from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlmodel import select, Session

from app.api.schema.customer_schema import CustomerSchema, GetAllCustomersResponse
from app.api.schema.shared.filtering import FilteringParams, get_filtering
from app.api.schema.shared.pagination import PaginationParams, get_pagination
from app.api.schema.shared.sorting import get_sorting, SortingParams
from app.core.models.main.customer import Customer
from app.core.repositories.customer_repository import CustomerRepository
from system.database.session import DatabaseSession
from system.database.settings import DatabaseId

customer_router = APIRouter(prefix="/customers")


@customer_router.get("")
async def get_all(
    main_database_session: Session = Depends(DatabaseSession(DatabaseId.MAIN)),
    customer_repository: CustomerRepository = Depends(),
    filtering: FilteringParams = Depends(get_filtering),
    sorting: SortingParams = Depends(get_sorting),
    pagination: PaginationParams = Depends(get_pagination(100, 300)),
) -> GetAllCustomersResponse:
    data_query = customer_repository.build_query(
        select(Customer),
        pagination.skip,
        pagination.limit,
        filtering.where,
        sorting.order_by,
    )
    data_result = main_database_session.exec(data_query)
    data = data_result.all()

    count_query = customer_repository.build_query(
        select(func.count(Customer.id)),
        where=filtering.where,
    )
    count_result = main_database_session.exec(count_query)
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
