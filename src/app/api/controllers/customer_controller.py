from fastapi import APIRouter, Depends

from app.api.schema.shared.pagination import PaginationParams, get_pagination

customer_router = APIRouter(prefix="/customers")


@customer_router.get("")
async def get_customers(
    pagination: PaginationParams = Depends(get_pagination(100, 300)),
) -> PaginationParams:
    return pagination
