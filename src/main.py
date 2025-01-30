import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status

from app.api.routes import api_router
from system.logging.setup import init_logging
from system.settings import get_settings
from system.uuids import generate_uuid


@asynccontextmanager
async def lifespan(_fastapi_app: FastAPI):
    settings = get_settings()
    logger = init_logging()

    logger.debug("Settings: %s", settings.model_dump_json(indent=2))
    logger.info("Starting %s", settings.app_name)
    yield
    logger.info("Stopping %s", settings.app_name)


fastapi_app = FastAPI(
    lifespan=lifespan,
    openapi_url=None,
)
fastapi_app.include_router(api_router)


@fastapi_app.middleware("http")
async def set_request_logger(request: Request, call_next):
    request_id = request.state.request_id
    request_logger = logging.getLogger(request_id)
    request.state.request_logger = request_logger
    response = await call_next(request)
    return response


@fastapi_app.middleware("http")
async def set_request_id(request: Request, call_next):
    request_id = generate_uuid("REQ")
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response


@fastapi_app.middleware("http")
async def remove_content_type_on_204(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == status.HTTP_204_NO_CONTENT:
        del response.headers["content-type"]
    return response
