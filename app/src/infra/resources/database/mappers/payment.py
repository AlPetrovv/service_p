from domain.entities.payment import PaymentEntity
from infra.resources.database.models.payment import Payment


class PaymentMapper:
    def to_entity(self, model: Payment) -> PaymentEntity:
        return PaymentEntity(
            id=model.id,
            transaction_id=model.transaction_id,
            account_id=model.account_id,
            user_id=model.user_id,
            amount=model.amount,
            created_at=model.created_at,
        )
