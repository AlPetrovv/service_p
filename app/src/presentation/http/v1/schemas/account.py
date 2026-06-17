from decimal import Decimal

from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: int
    balance: Decimal
