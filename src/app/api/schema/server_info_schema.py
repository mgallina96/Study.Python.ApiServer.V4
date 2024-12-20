from app.api.schema.shared.base import BaseSchema
from system.settings.models import Settings


class ServerInfoResponse(BaseSchema):
    app_version: str
    current_datetime: str
    app_settings: Settings


class GetServerInfoResponse(BaseSchema):
    data: ServerInfoResponse
