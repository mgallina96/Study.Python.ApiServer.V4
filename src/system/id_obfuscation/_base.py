from abc import ABC, abstractmethod
from typing import Self


class IIdObfuscator(ABC):
    @abstractmethod
    def encode(self, plain_id: int | None) -> str | None:
        raise NotImplementedError()

    @abstractmethod
    def decode(self, obfuscated_id: str | None) -> int | None:
        raise NotImplementedError()

    @abstractmethod
    def init(self, key: str) -> Self:
        raise NotImplementedError()


class IIdObfuscatorFactory(ABC):
    @abstractmethod
    def get_obfuscator(self, key: str) -> IIdObfuscator:
        raise NotImplementedError()
