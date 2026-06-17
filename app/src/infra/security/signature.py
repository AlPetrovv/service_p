import hashlib
import hmac
from decimal import Decimal
from uuid import UUID

from application.interfaces.security import ISignatureService


class Sha256SignatureService(ISignatureService):
    """Webhook signature service.

    The signature is the SHA256 hash of the object values concatenated in
    alphabetical order of their keys, followed by the secret key:
    ``{account_id}{amount}{transaction_id}{user_id}{secret_key}``.
    """

    def __init__(self, secret_key: str) -> None:
        self._secret_key = secret_key

    def sign(self, *, account_id: int, amount: Decimal, transaction_id: UUID, user_id: int) -> str:
        raw = f"{account_id}{amount}{transaction_id}{user_id}{self._secret_key}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def verify(
        self,
        *,
        account_id: int,
        amount: Decimal,
        transaction_id: UUID,
        user_id: int,
        signature: str,
    ) -> bool:
        expected = self.sign(
            account_id=account_id,
            amount=amount,
            transaction_id=transaction_id,
            user_id=user_id,
        )
        return hmac.compare_digest(expected, signature)
