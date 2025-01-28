from app.core.models.main._base import MainTable


class Customer(MainTable, table=True):
    name: str
    email: str
    phone: str
    address: str
