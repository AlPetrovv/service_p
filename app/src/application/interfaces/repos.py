from collections.abc import Sequence
from decimal import Decimal
from typing import Protocol
from uuid import UUID

from domain.entities.account import AccountEntity
from domain.entities.payment import PaymentEntity
from domain.entities.user import UserEntity
from domain.enums import UserRole


class IUserRepo(Protocol):
    """Repository interface for user persistence."""

    async def get_by_id(self, user_id: int) -> UserEntity | None: ...
    async def get_by_email(self, email: str) -> UserEntity | None: ...
    async def list_all(self) -> Sequence[UserEntity]: ...
    async def create(
        self,
        *,
        email: str,
        full_name: str,
        hashed_password: str,
        role: UserRole,
    ) -> UserEntity: ...
    async def update(
        self,
        user_id: int,
        *,
        email: str | None = None,
        full_name: str | None = None,
        hashed_password: str | None = None,
        role: UserRole | None = None,
    ) -> UserEntity: ...
    async def delete(self, user_id: int) -> None: ...


class IAccountRepo(Protocol):
    """Repository interface for account persistence."""

    async def get_by_id(self, account_id: int) -> AccountEntity | None: ...
    async def list_by_user_id(self, user_id: int) -> Sequence[AccountEntity]: ...
    async def list_all(self) -> Sequence[AccountEntity]: ...
    async def create(self, *, account_id: int, user_id: int, balance: Decimal) -> AccountEntity: ...
    async def add_balance(self, account_id: int, amount: Decimal) -> None: ...


class IPaymentRepo(Protocol):
    """Repository interface for payment persistence."""

    async def get_by_transaction_id(self, transaction_id: UUID) -> PaymentEntity | None: ...
    async def list_by_user_id(self, user_id: int) -> Sequence[PaymentEntity]: ...
    async def create(
        self,
        *,
        transaction_id: UUID,
        account_id: int,
        user_id: int,
        amount: Decimal,
    ) -> PaymentEntity: ...
