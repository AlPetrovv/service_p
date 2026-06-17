from application.dto.user import UserWithAccounts
from domain.entities.user import UserEntity
from presentation.http.v1.mappers.account import AccountApiMapper
from presentation.http.v1.schemas.user import UserResponse, UserWithAccountsResponse


class UserApiMapper:
    def __init__(self) -> None:
        self._account_mapper = AccountApiMapper()

    def to_response(self, entity: UserEntity) -> UserResponse:
        return UserResponse(
            id=entity.id,
            email=entity.email,
            full_name=entity.full_name,
            role=entity.role,
        )

    def to_with_accounts_response(self, item: UserWithAccounts) -> UserWithAccountsResponse:
        return UserWithAccountsResponse(
            id=item.user.id,
            email=item.user.email,
            full_name=item.user.full_name,
            role=item.user.role,
            accounts=[self._account_mapper.to_response(account) for account in item.accounts],
        )
