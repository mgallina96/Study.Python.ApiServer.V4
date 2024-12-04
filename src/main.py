from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import api_router
from system.logging.setup import init_logging
from system.settings.dependencies import get_settings


@asynccontextmanager
async def lifespan(_fastapi_app: FastAPI):
    logger = await init_logging()
    settings = await get_settings()
    logger.info(f"Starting {settings.app_name}")
    logger.debug(f"Settings: {settings.model_dump()}")

    logger.info(f"{settings.app_name} started")
    yield
    logger.info(f"{settings.app_name} stopped")


fastapi_app = FastAPI(
    lifespan=lifespan,
    openapi_url=None,
)
fastapi_app.include_router(api_router)
