from fastapi import APIRouter, Depends

from app.api.schema.server_info_schema import GetServerInfoResponseSchema
from app.api.schema.shared.base import ResponseSchema
from system.datetime.datetime_provider import DatetimeProvider
from system.settings.dependencies import get_settings
from system.settings.models import Settings
from system.version import APP_VERSION

server_info_router = APIRouter(prefix="/server-info")


@server_info_router.get("")
async def get_server_info(
    settings: Settings = Depends(get_settings),
    datetime_provider: DatetimeProvider = Depends(),
) -> ResponseSchema[GetServerInfoResponseSchema]:
    # Parse
    # Fetch / Process
    app_version = APP_VERSION
    current_datetime = await datetime_provider.now_tz()

    # Format
    return ResponseSchema[GetServerInfoResponseSchema](
        data=GetServerInfoResponseSchema(
            app_version=app_version,
            current_datetime=current_datetime.isoformat(),
            app_settings=settings.model_dump(),
        )
    )
