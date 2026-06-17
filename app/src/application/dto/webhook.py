from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass
class WebhookDTO:
    """Incoming payment-webhook payload from the third-party system."""

    transaction_id: UUID
    account_id: int
    user_id: int
    amount: Decimal
    signature: str
