from domain.entities.payment import PaymentEntity
from presentation.http.v1.schemas.payment import PaymentResponse


class PaymentApiMapper:
    def to_response(self, entity: PaymentEntity) -> PaymentResponse:
        return PaymentResponse(
            id=entity.id,
            transaction_id=entity.transaction_id,
            account_id=entity.account_id,
            amount=entity.amount,
            created_at=entity.created_at,
        )
