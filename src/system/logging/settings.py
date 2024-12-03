from enum import Enum

from pydantic import BaseModel, Json


class LoggingFormatter(Enum):
    PLAIN = "PLAIN"
    JSON = "JSON"


class LoggingSinkSettings(BaseModel):
    enabled: bool
    formatter: LoggingFormatter
    root_level: str


class LoggingSinkFileSettings(LoggingSinkSettings):
    path: str
    backup_count: int


class LoggingSettings(BaseModel):
    root_level: str
    format: str
    console: LoggingSinkSettings
    file: LoggingSinkFileSettings
    module_levels: Json[dict[str, str]]
