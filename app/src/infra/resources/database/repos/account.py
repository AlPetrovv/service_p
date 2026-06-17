from collections.abc import Sequence
from decimal import Decimal

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.repos import IAccountRepo
from domain.entities.account import AccountEntity
from infra.resources.database.mappers.account import AccountMapper
from infra.resources.database.models.account import Account


class DBAccountRepo(IAccountRepo):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._mapper = AccountMapper()

    async def get_by_id(self, account_id: int) -> AccountEntity | None:
        model = await self._session.get(Account, account_id)
        return self._mapper.to_entity(model) if model else None

    async def list_by_user_id(self, user_id: int) -> Sequence[AccountEntity]:
        result = await self._session.execute(
            select(Account).where(Account.user_id == user_id).order_by(Account.id)
        )
        return [self._mapper.to_entity(model) for model in result.scalars().all()]

    async def list_all(self) -> Sequence[AccountEntity]:
        result = await self._session.execute(select(Account).order_by(Account.id))
        return [self._mapper.to_entity(model) for model in result.scalars().all()]

    async def create(self, *, account_id: int, user_id: int, balance: Decimal) -> AccountEntity:
        model = Account(id=account_id, user_id=user_id, balance=balance)
        self._session.add(model)
        await self._session.flush()
        return self._mapper.to_entity(model)

    async def add_balance(self, account_id: int, amount: Decimal) -> None:
        await self._session.execute(
            update(Account).where(Account.id == account_id).values(balance=Account.balance + amount)
        )
