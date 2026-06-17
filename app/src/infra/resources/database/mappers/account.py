from domain.entities.account import AccountEntity
from infra.resources.database.models.account import Account


class AccountMapper:
    def to_entity(self, model: Account) -> AccountEntity:
        return AccountEntity(
            id=model.id,
            user_id=model.user_id,
            balance=model.balance,
            created_at=model.created_at,
        )
