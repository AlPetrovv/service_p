from dataclasses import dataclass, field

from domain.entities.account import AccountEntity
from domain.entities.user import UserEntity
from domain.enums import UserRole


@dataclass
class CreateUserDTO:
    """Payload for creating a user (admin)."""

    email: str
    password: str
    full_name: str
    role: UserRole = UserRole.USER


@dataclass
class UpdateUserDTO:
    """Partial update payload for a user (admin).

    ``None`` means "leave unchanged"; none of these fields are nullable.
    """

    email: str | None = None
    password: str | None = None
    full_name: str | None = None
    role: UserRole | None = None


@dataclass
class UserWithAccounts:
    """A user together with their accounts and balances."""

    user: UserEntity
    accounts: list[AccountEntity] = field(default_factory=list)
