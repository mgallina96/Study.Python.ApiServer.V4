from sqlalchemy import text
from sqlmodel import Session


def execute_raw_queries(session: Session, *queries: str) -> None:
    for query in queries:
        # noinspection PyTypeChecker
        session.exec(text(query))
