from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from application.interfaces.security import ITokenService
from domain.entities.user import UserEntity
from domain.exceptions import InvalidTokenError, NotAuthenticatedError, PermissionDeniedError
from infra.di.ioc import Container
from infra.resources.database.repos import UOW

bearer_scheme = HTTPBearer(auto_error=False)


@inject
async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    token_service: ITokenService = Depends(Provide[Container.security.token_service]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> UserEntity:
    if credentials is None or not credentials.credentials:
        raise NotAuthenticatedError
    payload = token_service.decode(credentials.credentials)
    async with uow:
        user = await uow.users.get_by_id(payload.user_id)
    if user is None:
        # Token is valid but the user no longer exists.
        raise InvalidTokenError
    return user


async def get_current_admin(current_user: UserEntity = Depends(get_current_user)) -> UserEntity:
    if not current_user.is_admin:
        raise PermissionDeniedError
    return current_user
