from datetime import datetime, timedelta, timezone

import jwt

from application.dto.auth import TokenPayload
from application.interfaces.security import ITokenService
from domain.enums import UserRole
from domain.exceptions import InvalidTokenError


class JWTTokenService(ITokenService):
    """Issues and validates HS256 JSON Web Tokens."""

    def __init__(self, secret: str, algorithm: str = "HS256", access_token_expire_minutes: int = 60) -> None:
        self._secret = secret
        self._algorithm = algorithm
        self._expire_minutes = access_token_expire_minutes

    def create_access_token(self, user_id: int, role: UserRole) -> str:
        now = datetime.now(tz=timezone.utc)
        payload = {
            "sub": str(user_id),
            "role": role.value,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self._expire_minutes)).timestamp()),
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def decode(self, token: str) -> TokenPayload:
        try:
            data = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            return TokenPayload(user_id=int(data["sub"]), role=UserRole(data["role"]))
        except (jwt.PyJWTError, KeyError, ValueError):
            raise InvalidTokenError from None
