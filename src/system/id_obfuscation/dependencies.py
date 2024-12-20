from system.id_obfuscation import (
    IIdObfuscatorFactory,
    SqidsObfuscatorFactory,
    DebugObfuscatorFactory,
)
from system.settings.dependencies import get_settings
from system.settings.models import Settings

_id_obfuscator_factory: IIdObfuscatorFactory


def init_id_obfuscation(settings: Settings = None) -> None:
    global _id_obfuscator_factory

    settings = settings or get_settings()

    if settings.sqids.enabled:
        _id_obfuscator_factory = SqidsObfuscatorFactory(
            settings.sqids.alphabet, settings.sqids.min_length
        )
    else:
        _id_obfuscator_factory = DebugObfuscatorFactory()


def get_id_obfuscator_factory() -> IIdObfuscatorFactory:
    return _id_obfuscator_factory
