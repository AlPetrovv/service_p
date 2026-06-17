"""seed test data

Revision ID: c308974154c6
Revises: 05bec75acdbc
Create Date: 2026-06-16 08:43:29.242813

"""
from datetime import datetime, timezone
from decimal import Decimal
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'c308974154c6'
down_revision: Union[str, Sequence[str], None] = '05bec75acdbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

#   user_password  -> USER_PASSWORD_HASH
#   admin_password -> ADMIN_PASSWORD_HASH
USER_PASSWORD_HASH = "$2b$12$GY6sZsrvJQi13yyryLzwYeGEoM07lotTiZZyP8fA35PQ4RZ1ni9pK"
ADMIN_PASSWORD_HASH = "$2b$12$TuCnU/5UKWwEKjjwUdoPxemgGN7M9yyFQ/0sLvspei6Fpk/spCX/."

SEEDED_AT = datetime(2026, 1, 1, tzinfo=timezone.utc)

_role_enum = postgresql.ENUM("user", "admin", name="user_role", create_type=False)

_users = sa.table(
    "users",
    sa.column("id", sa.BigInteger),
    sa.column("email", sa.String),
    sa.column("full_name", sa.String),
    sa.column("hashed_password", sa.String),
    sa.column("role", _role_enum),
    sa.column("created_at", sa.DateTime(timezone=True)),
)

_accounts = sa.table(
    "accounts",
    sa.column("id", sa.BigInteger),
    sa.column("user_id", sa.BigInteger),
    sa.column("balance", sa.Numeric),
    sa.column("created_at", sa.DateTime(timezone=True)),
)


def upgrade() -> None:
    """Insert the seed user, account and administrator."""
    op.bulk_insert(
        _users,
        [
            {
                "id": 1,
                "email": "user@example.com",
                "full_name": "Test User",
                "hashed_password": USER_PASSWORD_HASH,
                "role": "user",
                "created_at": SEEDED_AT,
            },
            {
                "id": 2,
                "email": "admin@example.com",
                "full_name": "Test Admin",
                "hashed_password": ADMIN_PASSWORD_HASH,
                "role": "admin",
                "created_at": SEEDED_AT,
            },
        ],
    )
    op.bulk_insert(
        _accounts,
        [
            {"id": 1, "user_id": 1, "balance": Decimal("0"), "created_at": SEEDED_AT},
        ],
    )
    op.execute("SELECT setval(pg_get_serial_sequence('users', 'id'), (SELECT MAX(id) FROM users))")
    op.execute("SELECT setval(pg_get_serial_sequence('accounts', 'id'), (SELECT MAX(id) FROM accounts))")


def downgrade() -> None:
    """Remove the seed data."""
    op.execute("DELETE FROM accounts WHERE id = 1")
    op.execute("DELETE FROM users WHERE id IN (1, 2)")
