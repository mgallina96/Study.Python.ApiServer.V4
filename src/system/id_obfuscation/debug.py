from typing import Self

from system.id_obfuscation._base import IIdObfuscator, IIdObfuscatorFactory


class DebugObfuscator(IIdObfuscator):
    def encode(self, plain_id: int | None) -> str | None:
        if plain_id is None:
            return None
        return str(plain_id)

    def decode(self, obfuscated_id: str | None) -> int | None:
        try:
            if obfuscated_id is None:
                return None
            return int(obfuscated_id)
        except ValueError:
            return -1

    def init(self, key: str) -> Self:
        return self


class DebugObfuscatorFactory(IIdObfuscatorFactory):
    def get_obfuscator(self, key: str) -> IIdObfuscator:
        return DebugObfuscator().init(key)
