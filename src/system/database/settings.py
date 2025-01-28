from enum import Enum

from pydantic import BaseModel, SecretStr


class DatabaseId(Enum):
    MAIN = "MAIN"


class DatabaseSettings(BaseModel):
    id: DatabaseId
    connection_string: str
    password: SecretStr
    pool_size: int
