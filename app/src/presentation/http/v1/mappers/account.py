from domain.entities.account import AccountEntity
from presentation.http.v1.schemas.account import AccountResponse


class AccountApiMapper:
    def to_response(self, entity: AccountEntity) -> AccountResponse:
        return AccountResponse(id=entity.id, balance=entity.balance)
