from decimal import Decimal
from uuid import UUID

from sqlalchemy import UUID as SAUUID
from sqlalchemy import BigInteger, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from infra.resources.database.models.base import Base
from infra.resources.database.models.mixins import CreatedAtMixin, IntPKMixin


class Payment(IntPKMixin, CreatedAtMixin, Base):
    __tablename__ = "payments"

    # Unique identifier of the transaction in the external system.
    transaction_id: Mapped[UUID] = mapped_column(SAUUID(as_uuid=True), unique=True, index=True)
    account_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("accounts.id", ondelete="CASCADE"),
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 2))
