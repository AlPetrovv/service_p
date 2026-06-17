from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class WebhookRequest(BaseModel):
    """Incoming payment webhook from the third-party payment system."""

    transaction_id: UUID
    account_id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    amount: Decimal = Field(gt=0)
    signature: str = Field(min_length=1)


class WebhookResponse(BaseModel):
    status: str
    transaction_id: UUID
    account_id: int
    user_id: int
    amount: Decimal
