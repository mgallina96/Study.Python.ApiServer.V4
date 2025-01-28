from uuid import UUID

from sqlmodel import SQLModel, Field


class BaseTable(SQLModel):
    id: UUID = Field(primary_key=True)

    class Config:
        from_attributes = True
