from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import api_router
from system.databases.connections import init_database_engines
from system.id_obfuscation.dependencies import init_id_obfuscation
from system.logging.setup import init_logging
from system.settings.dependencies import init_settings


@asynccontextmanager
async def lifespan(_fastapi_app: FastAPI):
    settings = await init_settings()
    logger = await init_logging()
    init_id_obfuscation(settings)
    init_database_engines(settings)

    logger.info("Starting %s", settings.app_name)
    yield
    logger.info("Stopping %s", settings.app_name)


fastapi_app = FastAPI(
    lifespan=lifespan,
    openapi_url=None,
)
fastapi_app.include_router(api_router)
