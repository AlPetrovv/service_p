from pydantic import BaseModel, EmailStr, Field

from domain.enums import UserRole
from presentation.http.v1.schemas.account import AccountResponse


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole


class UserWithAccountsResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    accounts: list[AccountResponse]


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)
    full_name: str = Field(min_length=1, max_length=255)
    role: UserRole = UserRole.USER


class UpdateUserRequest(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=6, max_length=72)
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    role: UserRole | None = None
