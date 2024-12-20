from system.datetime.settings import DatetimeSettings
from system.settings.dependencies import get_settings


async def get_datetime_settings() -> DatetimeSettings:
    return (get_settings()).datetime
