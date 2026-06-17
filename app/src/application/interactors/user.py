from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from application.dto.user import CreateUserDTO, UpdateUserDTO, UserWithAccounts
from application.interfaces.security import IPasswordHasher
from domain.entities.account import AccountEntity
from domain.entities.payment import PaymentEntity
from domain.entities.user import UserEntity
from domain.exceptions import EmailAlreadyExistsError, UserNotFoundError

if TYPE_CHECKING:
    from infra.resources.database.repos.uow import UOW


class CreateUserInteractor:
    def __init__(self, password_hasher: IPasswordHasher) -> None:
        self._password_hasher = password_hasher

    async def __call__(self, dto: CreateUserDTO, uow: "UOW") -> UserEntity:
        if await uow.users.get_by_email(dto.email):
            raise EmailAlreadyExistsError
        try:
            return await uow.users.create(
                email=dto.email,
                full_name=dto.full_name,
                hashed_password=self._password_hasher.hash(dto.password),
                role=dto.role,
            )
        except IntegrityError:
            await uow.rollback()
            raise EmailAlreadyExistsError from None


class UpdateUserInteractor:
    def __init__(self, password_hasher: IPasswordHasher) -> None:
        self._password_hasher = password_hasher

    async def __call__(self, user_id: int, dto: UpdateUserDTO, uow: "UOW") -> UserEntity:
        existing = await uow.users.get_by_id(user_id)
        if existing is None:
            raise UserNotFoundError

        if dto.email is not None and dto.email != existing.email:
            clash = await uow.users.get_by_email(dto.email)
            if clash is not None and clash.id != user_id:
                raise EmailAlreadyExistsError

        hashed_password = self._password_hasher.hash(dto.password) if dto.password is not None else None
        try:
            return await uow.users.update(
                user_id,
                email=dto.email,
                full_name=dto.full_name,
                hashed_password=hashed_password,
                role=dto.role,
            )
        except IntegrityError:
            await uow.rollback()
            raise EmailAlreadyExistsError from None


class DeleteUserInteractor:
    async def __call__(self, user_id: int, uow: "UOW") -> None:
        if await uow.users.get_by_id(user_id) is None:
            raise UserNotFoundError
        await uow.users.delete(user_id)


class GetUserInteractor:
    async def __call__(self, user_id: int, uow: "UOW") -> UserWithAccounts:
        user = await uow.users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError
        accounts = await uow.accounts.list_by_user_id(user_id)
        return UserWithAccounts(user=user, accounts=list(accounts))


class ListUsersInteractor:
    async def __call__(self, uow: "UOW") -> list[UserWithAccounts]:
        users = await uow.users.list_all()
        accounts = await uow.accounts.list_all()
        by_user: dict[int, list[AccountEntity]] = {}
        for account in accounts:
            by_user.setdefault(account.user_id, []).append(account)
        return [UserWithAccounts(user=user, accounts=by_user.get(user.id, [])) for user in users]


class GetMyAccountsInteractor:
    async def __call__(self, user_id: int, uow: "UOW") -> list[AccountEntity]:
        return list(await uow.accounts.list_by_user_id(user_id))


class GetMyPaymentsInteractor:
    async def __call__(self, user_id: int, uow: "UOW") -> list[PaymentEntity]:
        return list(await uow.payments.list_by_user_id(user_id))
