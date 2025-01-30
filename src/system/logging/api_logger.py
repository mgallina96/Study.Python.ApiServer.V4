from logging import Logger

from fastapi import Request
from pydantic import BaseModel


class RequestLog(BaseModel):
    input: dict

    def __str__(self):
        return self.model_dump_json(indent=2)


def get_request_logger(request: Request) -> Logger:
    return request.state.request_logger
