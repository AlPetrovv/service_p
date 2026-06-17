class DomainError(Exception):
    """Base domain error carrying the HTTP status and message it maps to."""

    status_code: int = 500
    detail: str = "Internal error"

    def __init__(self, detail: str | None = None) -> None:
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class InvalidCredentialsError(DomainError):
    status_code = 401
    detail = "Invalid email or password"


class NotAuthenticatedError(DomainError):
    status_code = 401
    detail = "Not authenticated"


class InvalidTokenError(DomainError):
    status_code = 401
    detail = "Invalid or expired token"


class PermissionDeniedError(DomainError):
    status_code = 403
    detail = "Not enough permissions"


class UserNotFoundError(DomainError):
    status_code = 404
    detail = "User not found"


class AccountNotFoundError(DomainError):
    status_code = 404
    detail = "Account not found"


class EmailAlreadyExistsError(DomainError):
    status_code = 409
    detail = "User with this email already exists"


class AccountOwnershipError(DomainError):
    status_code = 409
    detail = "Account belongs to another user"


class InvalidSignatureError(DomainError):
    status_code = 400
    detail = "Invalid signature"
