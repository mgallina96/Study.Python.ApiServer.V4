import datetime
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

from pythonjsonlogger import jsonlogger

from system.settings.dependencies import get_logging_settings


# noinspection PyPep8Naming,PyUnusedLocal
def _formatTime(  # pylint: disable=invalid-name
    record: logging.LogRecord,
    datefmt=None,  # pylint: disable=unused-argument
):
    """Override the original formatTime method to use a timezone-aware
    timestamp, compatible with both ISO 8601 and RFC 3339."""
    return (
        datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc)
        .astimezone()
        .isoformat(timespec="milliseconds")
    )


async def init_logging() -> None:
    settings = await get_logging_settings()

    logger = logging.getLogger()
    logger.setLevel(settings.root_level.upper())

    json_formatter = jsonlogger.JsonFormatter(fmt=settings.logger__root__format)
    json_formatter.formatTime = _formatTime
    plain_formatter = logging.Formatter(fmt=settings.logger__root__format)
    plain_formatter.formatTime = _formatTime

    if settings.file.enabled:
        file_handler = TimedRotatingFileHandler(
            settings.file.path,
            when="midnight",
            backupCount=settings.file.backup_count,
        )
        file_handler.setFormatter(json_formatter)
        logger.addHandler(file_handler)

    if settings.console.enabled:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(plain_formatter)
        logger.addHandler(console_handler)

    for module, level in settings.module_levels.items():
        logging.getLogger(module).setLevel(level.upper())
