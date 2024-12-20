import logging
import random
from logging import Logger
from typing import Self
from pydantic import BaseModel
from sqids import Sqids


from system.id_obfuscation._base import IIdObfuscator, IIdObfuscatorFactory

SQIDS_DECODE_ERROR = "Error decoding id=%s; reason=%s"


class SqidsObfuscationSettings(BaseModel):
    enabled: bool
    alphabet: str
    min_length: int


class SqidsObfuscator(IIdObfuscator):
    _logger: Logger
    _sqids: Sqids
    _alphabet: str
    _min_length: int

    def __init__(self, alphabet: str, min_length: int):
        self._logger = logging.getLogger("id_obfuscation.sqids")
        self._alphabet = alphabet
        self._min_length = min_length

    def init(self, key: str) -> Self:
        random.seed(key)
        custom_alphabet = list(self._alphabet).copy()
        random.shuffle(custom_alphabet)
        custom_alphabet = "".join(custom_alphabet)
        self._sqids = Sqids(
            alphabet=custom_alphabet,
            min_length=self._min_length,
        )
        return self

    def encode(self, plain_id: int | None) -> str | None:
        if plain_id is None:
            return None
        return self._sqids.encode([plain_id])

    def decode(self, obfuscated_id: str | None) -> int | None:
        if obfuscated_id is None:
            return None
        plain_id = self._sqids.decode(obfuscated_id)
        if len(plain_id) != 1:
            self._logger.warning(
                SQIDS_DECODE_ERROR, obfuscated_id, "len(plain_id) != 1"
            )
            return -1
        plain_id = plain_id[0]
        if plain_id < -(2**31) or plain_id > (2**31) - 1:
            self._logger.warning(
                SQIDS_DECODE_ERROR,
                obfuscated_id,
                "plain_id out of int32 range, probably due to hash collision",
            )
            return -1
        return plain_id


class SqidsObfuscatorFactory(IIdObfuscatorFactory):
    _logger: Logger
    _obfuscators: dict[str, SqidsObfuscator]
    _alphabet: str
    _min_length: int

    def __init__(self, alphabet: str, min_length: int):
        self._obfuscators = {}
        self._alphabet = alphabet
        self._min_length = min_length
        self._logger = logging.getLogger("id_obfuscation.sqids")

    def get_obfuscator(self, key: str) -> SqidsObfuscator:
        self._logger.debug("Getting obfuscator for key=%s", key)
        if key not in self._obfuscators:
            self._obfuscators[key] = SqidsObfuscator(
                self._alphabet, self._min_length
            ).init(key)
        return self._obfuscators[key]
