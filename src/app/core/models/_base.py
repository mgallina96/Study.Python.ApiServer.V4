from sqlmodel import SQLModel, Field


class BaseTable(SQLModel):
    id: int | None = Field(default=None, primary_key=True)

    class Config:
        from_attributes = True
