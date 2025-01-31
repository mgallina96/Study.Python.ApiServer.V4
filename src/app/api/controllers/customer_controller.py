from logging import Logger

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlmodel import select, Session

from app.api.schema.customer_schema import (
    CustomerSchema,
    GetAllCustomersResponse,
    GetCustomerResponse,
)
from app.api.schema.shared.base import CountMeta
from app.api.schema.shared.filtering import FilteringParams, get_filtering
from app.api.schema.shared.pagination import PaginationParams, get_pagination
from app.api.schema.shared.sorting import get_sorting, SortingParams
from app.core.models.main.customer import Customer
from system.database.session import DatabaseSession
from system.database.settings import DatabaseId
from system.logging.api_logger import get_request_logger, RequestLog

customer_router = APIRouter(prefix="/customers")


@customer_router.get("")
async def get_all(
    logger: Logger = Depends(get_request_logger),
    main_database_session: Session = Depends(DatabaseSession(DatabaseId.MAIN)),
    filtering: FilteringParams = Depends(get_filtering),
    sorting: SortingParams = Depends(get_sorting),
    pagination: PaginationParams = Depends(get_pagination(100, 300)),
) -> GetAllCustomersResponse:
    logger.debug(
        RequestLog(
            input={
                "filtering": filtering,
                "sorting": sorting,
                "pagination": pagination,
            }
        )
    )

    data = main_database_session.exec(
        CustomerSchema.build_query(
            select(Customer),
            pagination.skip,
            pagination.limit,
            filtering.where,
            sorting.order_by,
        )
    ).all()

    count = main_database_session.exec(
        CustomerSchema.build_query(
            select(func.count(Customer.id)),
            where=filtering.where,
        )
    ).one()

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


@customer_router.get("/{customer_id}")
async def get(
    customer_id: str,
    logger: Logger = Depends(get_request_logger),
    main_database_session: Session = Depends(DatabaseSession(DatabaseId.MAIN)),
) -> GetCustomerResponse:
    logger.debug(RequestLog(input={"customer_id": customer_id}))

    data = main_database_session.get(Customer, customer_id)
    if not data:
        raise HTTPException(status_code=404, detail="Customer not found")

    return GetCustomerResponse(
        data=CustomerSchema(
            id=data.id,
            name=data.name,
            email=data.email,
            phone=data.phone,
            address=data.address,
        )
    )
