from decimal import Decimal
from typing import Protocol
from uuid import UUID

from application.dto.auth import TokenPayload
from domain.enums import UserRole


class IPasswordHasher(Protocol):
    """Hashes and verifies user passwords."""

    def hash(self, password: str) -> str: ...
    def verify(self, password: str, hashed: str) -> bool: ...


class ITokenService(Protocol):
    """Issues and decodes access tokens."""

    def create_access_token(self, user_id: int, role: UserRole) -> str: ...
    def decode(self, token: str) -> TokenPayload: ...


class ISignatureService(Protocol):
    """Builds and verifies third-party webhook signatures."""

    def sign(self, *, account_id: int, amount: Decimal, transaction_id: UUID, user_id: int) -> str: ...
    def verify(
        self,
        *,
        account_id: int,
        amount: Decimal,
        transaction_id: UUID,
        user_id: int,
        signature: str,
    ) -> bool: ...
