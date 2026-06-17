from domain.entities.user import UserEntity
from domain.enums import UserRole
from infra.resources.database.models.user import User


class UserMapper:
    def to_entity(self, model: User) -> UserEntity:
        return UserEntity(
            id=model.id,
            email=model.email,
            full_name=model.full_name,
            hashed_password=model.hashed_password,
            role=UserRole(model.role),
            created_at=model.created_at,
        )
