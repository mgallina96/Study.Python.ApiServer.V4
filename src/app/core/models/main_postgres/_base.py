from sqlalchemy import MetaData

from app.core.models._base import BaseTable

main_metadata = MetaData(schema="main")


class MainPostgresTable(BaseTable):
    metadata = main_metadata
