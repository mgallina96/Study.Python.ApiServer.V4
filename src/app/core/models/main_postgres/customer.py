from app.core.models.main_postgres._base import MainPostgresTable


class Customer(MainPostgresTable, table=True):
    name: str
    email: str
    phone: str
    address: str
