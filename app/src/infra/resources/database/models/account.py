from decimal import Decimal

from sqlalchemy import BigInteger, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from infra.resources.database.models.base import Base
from infra.resources.database.models.mixins import CreatedAtMixin


class Account(CreatedAtMixin, Base):
    __tablename__ = "accounts"

    # The account id is assigned by the external payment system, not generated locally.
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(20, 2),
        default=Decimal("0"),
        server_default="0",
        nullable=False,
    )
