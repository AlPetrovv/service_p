from typing import TYPE_CHECKING

from application.dto.auth import LoginDTO
from application.interfaces.security import IPasswordHasher, ITokenService
from domain.exceptions import InvalidCredentialsError

if TYPE_CHECKING:
    from infra.resources.database.repos.uow import UOW


class LoginInteractor:
    """Authenticates a user by email/password and issues an access token."""

    def __init__(self, password_hasher: IPasswordHasher, token_service: ITokenService) -> None:
        self._password_hasher = password_hasher
        self._token_service = token_service

    async def __call__(self, dto: LoginDTO, uow: "UOW") -> str:
        user = await uow.users.get_by_email(dto.email)
        if user is None or not self._password_hasher.verify(dto.password, user.hashed_password):
            raise InvalidCredentialsError
        return self._token_service.create_access_token(user.id, user.role)
