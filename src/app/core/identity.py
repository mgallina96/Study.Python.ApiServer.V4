from pydantic import BaseModel, SecretStr
from fastapi import Request, Depends
from pydantic import SecretStr
from sqlalchemy.orm import Session


class Identity(BaseModel):
    user: User | None
    is_system: bool
    access_token: SecretStr | None = None

    @property
    def is_authenticated(self) -> bool:
        return self.is_system or self.user is not None


ANONYMOUS_IDENTITY = Identity(user=None, is_system=False)
SYSTEM_IDENTITY = Identity(user=None, is_system=True)


# Separating the get_identity function from the require_user_authentication function
# allows for better testability of the get_identity function.
def _get_authorization_header(request: Request) -> str | None:
    return request.headers.get("Authorization")


async def get_identity(
    authorization_header: str | None = Depends(_get_authorization_header),
    db_session: Session = Depends(postgres_main_controller.get_db_session),
    auth_service: IAuthService = Depends(),
    integer_encryption_service: IIntegerEncryptionService = Depends(),
    user_service: IUserService = Depends(),
) -> Identity:
    if authorization_header is None:
        return ANONYMOUS_IDENTITY
    access_token = authorization_header.split(" ")[1]

    try:
        jwt_payload = await auth_service.validate_access_token(access_token)
    except InvalidTokenError:
        return ANONYMOUS_IDENTITY

    user_id = integer_encryption_service.decrypt(jwt_payload.user_id)
    user = await user_service.get(
        db_session,
        SYSTEM_IDENTITY,
        entity_id=auth_user_id_obfuscator.encode(user_id),
    )
    if user is not None:
        return Identity(
            user=user, is_system=False, access_token=SecretStr(access_token)
        )

    return ANONYMOUS_IDENTITY
