from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from application.dto.user import CreateUserDTO, UpdateUserDTO
from application.interactors.user import (
    CreateUserInteractor,
    DeleteUserInteractor,
    GetUserInteractor,
    ListUsersInteractor,
    UpdateUserInteractor,
)
from infra.di.ioc import Container
from infra.resources.database.repos import UOW
from presentation.http.authentication import get_current_admin
from presentation.http.v1.mappers.user import UserApiMapper
from presentation.http.v1.schemas.user import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
    UserWithAccountsResponse,
)

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(get_current_admin)])


@router.get("/users", summary="List users with their accounts and balances")
@inject
async def list_users(
    interactor: ListUsersInteractor = Depends(Provide[Container.interactors.list_users]),
    mapper: UserApiMapper = Depends(Provide[Container.mappers.user_mapper]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> list[UserWithAccountsResponse]:
    async with uow:
        items = await interactor(uow=uow)
    return [mapper.to_with_accounts_response(item) for item in items]


@router.get("/users/{user_id}", summary="Get a user with their accounts and balances")
@inject
async def get_user(
    user_id: int,
    interactor: GetUserInteractor = Depends(Provide[Container.interactors.get_user]),
    mapper: UserApiMapper = Depends(Provide[Container.mappers.user_mapper]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> UserWithAccountsResponse:
    async with uow:
        item = await interactor(user_id=user_id, uow=uow)
    return mapper.to_with_accounts_response(item)


@router.post("/users", status_code=status.HTTP_201_CREATED, summary="Create a user")
@inject
async def create_user(
    body: CreateUserRequest,
    interactor: CreateUserInteractor = Depends(Provide[Container.interactors.create_user]),
    mapper: UserApiMapper = Depends(Provide[Container.mappers.user_mapper]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> UserResponse:
    dto = CreateUserDTO(
        email=str(body.email),
        password=body.password,
        full_name=body.full_name,
        role=body.role,
    )
    async with uow:
        user = await interactor(dto=dto, uow=uow)
    return mapper.to_response(user)


@router.patch("/users/{user_id}", summary="Update a user")
@inject
async def update_user(
    user_id: int,
    body: UpdateUserRequest,
    interactor: UpdateUserInteractor = Depends(Provide[Container.interactors.update_user]),
    mapper: UserApiMapper = Depends(Provide[Container.mappers.user_mapper]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> UserResponse:
    dto = UpdateUserDTO(
        email=str(body.email) if body.email is not None else None,
        password=body.password,
        full_name=body.full_name,
        role=body.role,
    )
    async with uow:
        user = await interactor(user_id=user_id, dto=dto, uow=uow)
    return mapper.to_response(user)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a user")
@inject
async def delete_user(
    user_id: int,
    interactor: DeleteUserInteractor = Depends(Provide[Container.interactors.delete_user]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> None:
    async with uow:
        await interactor(user_id=user_id, uow=uow)
