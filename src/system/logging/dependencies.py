from system.logging.settings import LoggingSettings
from system.settings.dependencies import get_settings


async def get_logging_settings() -> LoggingSettings:
    return (get_settings()).logging
