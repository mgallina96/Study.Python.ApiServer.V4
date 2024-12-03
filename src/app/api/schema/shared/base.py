from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


DataSchemaT = TypeVar("DataSchemaT", bound=BaseSchema)


class ResponseSchema(BaseSchema, Generic[DataSchemaT]):
    data: DataSchemaT
