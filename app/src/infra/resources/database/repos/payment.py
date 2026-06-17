from collections.abc import Sequence
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.repos import IPaymentRepo
from domain.entities.payment import PaymentEntity
from infra.resources.database.mappers.payment import PaymentMapper
from infra.resources.database.models.payment import Payment


class DBPaymentRepo(IPaymentRepo):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._mapper = PaymentMapper()

    async def get_by_transaction_id(self, transaction_id: UUID) -> PaymentEntity | None:
        result = await self._session.execute(
            select(Payment).where(Payment.transaction_id == transaction_id)
        )
        model = result.scalar_one_or_none()
        return self._mapper.to_entity(model) if model else None

    async def list_by_user_id(self, user_id: int) -> Sequence[PaymentEntity]:
        result = await self._session.execute(
            select(Payment).where(Payment.user_id == user_id).order_by(Payment.created_at, Payment.id)
        )
        return [self._mapper.to_entity(model) for model in result.scalars().all()]

    async def create(
        self,
        *,
        transaction_id: UUID,
        account_id: int,
        user_id: int,
        amount: Decimal,
    ) -> PaymentEntity:
        model = Payment(transaction_id=transaction_id, account_id=account_id, user_id=user_id, amount=amount)
        self._session.add(model)
        await self._session.flush()
        return self._mapper.to_entity(model)
