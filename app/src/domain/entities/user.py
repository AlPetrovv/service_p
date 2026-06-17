from dataclasses import dataclass
from datetime import datetime

from domain.entities.base import Entity
from domain.enums import UserRole


@dataclass(kw_only=True)
class UserEntity(Entity[int]):
    email: str
    full_name: str
    hashed_password: str
    role: UserRole
    created_at: datetime

    @property
    def is_admin(self) -> bool:
        return self.role is UserRole.ADMIN
