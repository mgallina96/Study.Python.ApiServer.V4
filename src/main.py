from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import api_router
from system.logging.setup import init_logging
from system.settings import get_settings


@asynccontextmanager
async def lifespan(_fastapi_app: FastAPI):
    settings = get_settings()
    logger = init_logging()

    logger.info("Starting %s", settings.app_name)
    yield
    logger.info("Stopping %s", settings.app_name)


fastapi_app = FastAPI(
    lifespan=lifespan,
    openapi_url=None,
)
fastapi_app.include_router(api_router)
