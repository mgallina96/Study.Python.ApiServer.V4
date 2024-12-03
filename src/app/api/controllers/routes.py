from fastapi import APIRouter

from app.api.controllers.customer_controller import customer_router
from app.api.controllers.server_info_controller import server_info_router

v4_router = APIRouter(prefix="/v4")
v4_router.include_router(server_info_router)
v4_router.include_router(customer_router)
