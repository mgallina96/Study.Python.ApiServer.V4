from pydantic import BaseModel, SecretStr


class EncryptionSettings(BaseModel):
    key: SecretStr
    iv: SecretStr
