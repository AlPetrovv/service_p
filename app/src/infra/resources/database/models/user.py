from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from domain.enums import UserRole
from infra.resources.database.models.base import Base
from infra.resources.database.models.mixins import CreatedAtMixin, IntPKMixin


class User(IntPKMixin, CreatedAtMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name="user_role",
            values_callable=lambda enum: [member.value for member in enum],
        ),
        default=UserRole.USER,
        server_default=UserRole.USER.value,
        index=True,
    )
