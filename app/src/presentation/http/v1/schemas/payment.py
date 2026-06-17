from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class PaymentResponse(BaseModel):
    id: int
    transaction_id: UUID
    account_id: int
    amount: Decimal
    created_at: datetime
