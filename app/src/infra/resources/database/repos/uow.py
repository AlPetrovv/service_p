from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.repos import IAccountRepo, IPaymentRepo, IUserRepo
from infra.resources.database.manager import DatabaseSessionManager
from infra.resources.database.repos.account import DBAccountRepo
from infra.resources.database.repos.payment import DBPaymentRepo
from infra.resources.database.repos.user import DBUserRepo


class UOW:
    """Unit of work: owns a session and commits/rolls back on context exit."""

    def __init__(self, db_manager: DatabaseSessionManager) -> None:
        self._db_manager = db_manager
        self._session_ctx = None
        self.session: AsyncSession = None  # type: ignore[assignment]

    async def __aenter__(self) -> "UOW":
        self._session_ctx = self._db_manager.session()
        self.session = await self._session_ctx.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.session.commit()
        await self._session_ctx.__aexit__(exc_type, exc_val, exc_tb)

    async def flush(self) -> None:
        await self.session.flush()

    async def rollback(self) -> None:
        await self.session.rollback()

    @property
    def users(self) -> IUserRepo:
        return DBUserRepo(self.session)

    @property
    def accounts(self) -> IAccountRepo:
        return DBAccountRepo(self.session)

    @property
    def payments(self) -> IPaymentRepo:
        return DBPaymentRepo(self.session)
