from enum import Enum

from pydantic import BaseModel, SecretStr


class DatabaseSettings(BaseModel):
    connection_string: str
    password: SecretStr
    pool_size: int


class DatabaseConnections(Enum):
    MAIN_POSTGRES = "main_postgres"
