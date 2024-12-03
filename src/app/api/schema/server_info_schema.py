from app.api.schema.shared.base import BaseSchema


class GetServerInfoResponseSchema(BaseSchema):
    app_version: str
    current_datetime: str
    app_settings: dict
