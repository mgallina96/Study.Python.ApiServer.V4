from logging import Logger

from fastapi import APIRouter, Depends, status
from sqlalchemy import func, Select
from sqlmodel import select, Session

from app.api.schema.customer_schema import (
    CustomerSchema,
    GetAllCustomersResponse,
    GetCustomerResponse,
    CreateCustomerRequest,
)
from app.api.schema.shared.base import CountMeta
from app.api.schema.shared.errors import ApiError
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
        raise ApiError(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Customer not found",
            detail=f"Customer not found with id: {customer_id}",
        )

    return GetCustomerResponse(
        data=CustomerSchema(
            id=data.id,
            name=data.name,
            email=data.email,
            phone=data.phone,
            address=data.address,
        )
    )


@customer_router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    body: CreateCustomerRequest,
    logger: Logger = Depends(get_request_logger),
    main_database_session: Session = Depends(DatabaseSession(DatabaseId.MAIN)),
) -> GetCustomerResponse:
    logger.debug(RequestLog(input={"body": body}))

    data_query: Select = select(Customer).where(Customer.email == body.email)
    data = main_database_session.exec(data_query).first()
    if data:
        raise ApiError(
            status_code=status.HTTP_409_CONFLICT,
            message="Customer already exists",
            detail=f"Customer already exists with email: {body.email}",
        )

    data = Customer(
        name=body.name,
        email=body.email,
        phone=body.phone,
        address=body.address,
    )
    main_database_session.add(data)

    return GetCustomerResponse(
        data=CustomerSchema(
            id=data.id,
            name=data.name,
            email=data.email,
            phone=data.phone,
            address=data.address,
        )
    )


@customer_router.put("/{customer_id}")
async def update(
    customer_id: str,
    body: CreateCustomerRequest,
    logger: Logger = Depends(get_request_logger),
    main_database_session: Session = Depends(DatabaseSession(DatabaseId.MAIN)),
) -> GetCustomerResponse:
    logger.debug(RequestLog(input={"customer_id": customer_id, "body": body}))

    data_query: Select = select(Customer).where(
        Customer.id != customer_id, Customer.email == body.email
    )
    data = main_database_session.exec(data_query).first()
    if data:
        raise ApiError(
            status_code=status.HTTP_409_CONFLICT,
            message="Customer already exists",
            detail=f"Customer already exists with email: {body.email}",
        )

    data = main_database_session.get(Customer, customer_id)
    if not data:
        raise ApiError(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Customer not found",
            detail=f"Customer not found with id: {customer_id}",
        )

    data.name = body.name
    data.email = body.email
    data.phone = body.phone
    data.address = body.address

    return GetCustomerResponse(
        data=CustomerSchema(
            id=data.id,
            name=data.name,
            email=data.email,
            phone=data.phone,
            address=data.address,
        )
    )


@customer_router.delete("/{customer_id}")
async def delete(
    customer_id: str,
    logger: Logger = Depends(get_request_logger),
    main_database_session: Session = Depends(DatabaseSession(DatabaseId.MAIN)),
) -> GetCustomerResponse:
    logger.debug(RequestLog(input={"customer_id": customer_id}))

    data = main_database_session.get(Customer, customer_id)
    if not data:
        raise ApiError(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Customer not found",
            detail=f"Customer not found with id: {customer_id}",
        )

    main_database_session.delete(data)

    return GetCustomerResponse(
        data=CustomerSchema(
            id=data.id,
            name=data.name,
            email=data.email,
            phone=data.phone,
            address=data.address,
        )
    )
