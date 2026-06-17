from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.entities.base import Entity


@dataclass(kw_only=True)
class AccountEntity(Entity[int]):
    user_id: int
    balance: Decimal
    created_at: datetime
