from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from domain.entities.base import Entity


@dataclass(kw_only=True)
class PaymentEntity(Entity[int]):
    transaction_id: UUID
    account_id: int
    user_id: int
    amount: Decimal
    created_at: datetime
