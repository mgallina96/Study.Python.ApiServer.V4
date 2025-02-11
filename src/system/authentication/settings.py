from pydantic import BaseModel, SecretStr

from system.encryption import EncryptionSettings


class TokenSettings(BaseModel):
    secret: SecretStr
    lifetime_seconds: int
    payload_encryption: EncryptionSettings


class AuthSettings(BaseModel):
    jwt_algorithm: str
    access_token: TokenSettings
    refresh_token: TokenSettings
