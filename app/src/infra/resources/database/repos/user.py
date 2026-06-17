from collections.abc import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.repos import IUserRepo
from domain.entities.user import UserEntity
from domain.enums import UserRole
from domain.exceptions import UserNotFoundError
from infra.resources.database.mappers.user import UserMapper
from infra.resources.database.models.user import User


class DBUserRepo(IUserRepo):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._mapper = UserMapper()

    async def get_by_id(self, user_id: int) -> UserEntity | None:
        model = await self._session.get(User, user_id)
        return self._mapper.to_entity(model) if model else None

    async def get_by_email(self, email: str) -> UserEntity | None:
        result = await self._session.execute(select(User).where(User.email == email))
        model = result.scalar_one_or_none()
        return self._mapper.to_entity(model) if model else None

    async def list_all(self) -> Sequence[UserEntity]:
        result = await self._session.execute(select(User).order_by(User.id))
        return [self._mapper.to_entity(model) for model in result.scalars().all()]

    async def create(
        self,
        *,
        email: str,
        full_name: str,
        hashed_password: str,
        role: UserRole,
    ) -> UserEntity:
        model = User(email=email, full_name=full_name, hashed_password=hashed_password, role=role)
        self._session.add(model)
        await self._session.flush()
        return self._mapper.to_entity(model)

    async def update(
        self,
        user_id: int,
        *,
        email: str | None = None,
        full_name: str | None = None,
        hashed_password: str | None = None,
        role: UserRole | None = None,
    ) -> UserEntity:
        model = await self._session.get(User, user_id)
        if model is None:
            raise UserNotFoundError
        if email is not None:
            model.email = email
        if full_name is not None:
            model.full_name = full_name
        if hashed_password is not None:
            model.hashed_password = hashed_password
        if role is not None:
            model.role = role
        await self._session.flush()
        return self._mapper.to_entity(model)

    async def delete(self, user_id: int) -> None:
        await self._session.execute(delete(User).where(User.id == user_id))
