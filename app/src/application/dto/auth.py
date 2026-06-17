from dataclasses import dataclass

from domain.enums import UserRole


@dataclass
class LoginDTO:
    """Credentials supplied to the login interactor."""

    email: str
    password: str


@dataclass
class TokenPayload:
    """Decoded contents of an access token."""

    user_id: int
    role: UserRole
