from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from application.dto.webhook import WebhookDTO
from application.interfaces.security import ISignatureService
from domain.entities.payment import PaymentEntity
from domain.exceptions import AccountOwnershipError, InvalidSignatureError, UserNotFoundError

if TYPE_CHECKING:
    from infra.resources.database.repos.uow import UOW


class ProcessWebhookInteractor:

    def __init__(self, signature_service: ISignatureService) -> None:
        self._signature_service = signature_service

    async def __call__(self, dto: WebhookDTO, uow: "UOW") -> PaymentEntity:
        if not self._signature_service.verify(
            account_id=dto.account_id,
            amount=dto.amount,
            transaction_id=dto.transaction_id,
            user_id=dto.user_id,
            signature=dto.signature,
        ):
            raise InvalidSignatureError

        # Transactions are unique: a transaction_id is credited exactly once.
        existing = await uow.payments.get_by_transaction_id(dto.transaction_id)
        if existing is not None:
            return existing

        user = await uow.users.get_by_id(dto.user_id)
        if user is None:
            raise UserNotFoundError

        try:
            account = await uow.accounts.get_by_id(dto.account_id)
            if account is None:
                await uow.accounts.create(
                    account_id=dto.account_id,
                    user_id=dto.user_id,
                    balance=Decimal("0"),
                )
            elif account.user_id != dto.user_id:
                raise AccountOwnershipError

            payment = await uow.payments.create(
                transaction_id=dto.transaction_id,
                account_id=dto.account_id,
                user_id=dto.user_id,
                amount=dto.amount,
            )
            await uow.accounts.add_balance(dto.account_id, dto.amount)
            await uow.flush()
        except IntegrityError:
            # Concurrent delivery of the same transaction raced us — stay idempotent.
            await uow.rollback()
            existing = await uow.payments.get_by_transaction_id(dto.transaction_id)
            if existing is not None:
                return existing
            raise

        return payment
