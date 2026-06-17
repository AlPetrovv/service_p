from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from application.interactors.auth import LoginInteractor
from application.interactors.user import (
    CreateUserInteractor,
    DeleteUserInteractor,
    GetMyAccountsInteractor,
    GetMyPaymentsInteractor,
    GetUserInteractor,
    ListUsersInteractor,
    UpdateUserInteractor,
)
from application.interactors.webhook import ProcessWebhookInteractor
from infra.core.config import settings
from infra.resources.database.manager import DatabaseSessionManager
from infra.resources.database.repos import UOW
from infra.security.jwt import JWTTokenService
from infra.security.password import BcryptPasswordHasher
from infra.security.signature import Sha256SignatureService
from presentation.http.v1.mappers.account import AccountApiMapper
from presentation.http.v1.mappers.payment import PaymentApiMapper
from presentation.http.v1.mappers.user import UserApiMapper


class DatabaseContainer(DeclarativeContainer):
    config = providers.Configuration()

    engine_kwargs = providers.Dict(
        echo=config.db.echo,
        echo_pool=config.db.echo_pool,
        pool_size=config.db.pool_size,
        max_overflow=config.db.max_overflow,
        pool_pre_ping=config.db.pool_pre_ping,
    )

    db_manager = providers.Singleton(
        DatabaseSessionManager,
        db_url=config.db.url,
        engine_kwargs=engine_kwargs,
    )
    uow = providers.Factory(UOW, db_manager=db_manager)


class SecurityContainer(DeclarativeContainer):
    config = providers.Configuration()

    password_hasher = providers.Singleton(BcryptPasswordHasher)
    token_service = providers.Singleton(
        JWTTokenService,
        secret=config.jwt.secret,
        algorithm=config.jwt.algorithm,
        access_token_expire_minutes=config.jwt.access_token_expire_minutes,
    )
    signature_service = providers.Singleton(
        Sha256SignatureService,
        secret_key=config.webhook_secret_key,
    )


class InteractorsContainer(DeclarativeContainer):
    password_hasher = providers.Dependency()
    token_service = providers.Dependency()
    signature_service = providers.Dependency()

    login = providers.Factory(
        LoginInteractor,
        password_hasher=password_hasher,
        token_service=token_service,
    )
    create_user = providers.Factory(CreateUserInteractor, password_hasher=password_hasher)
    update_user = providers.Factory(UpdateUserInteractor, password_hasher=password_hasher)
    delete_user = providers.Factory(DeleteUserInteractor)
    get_user = providers.Factory(GetUserInteractor)
    list_users = providers.Factory(ListUsersInteractor)
    my_accounts = providers.Factory(GetMyAccountsInteractor)
    my_payments = providers.Factory(GetMyPaymentsInteractor)
    process_webhook = providers.Factory(ProcessWebhookInteractor, signature_service=signature_service)


class MappersContainer(DeclarativeContainer):
    user_mapper = providers.Factory(UserApiMapper)
    account_mapper = providers.Factory(AccountApiMapper)
    payment_mapper = providers.Factory(PaymentApiMapper)


class Container(DeclarativeContainer):
    config = providers.Configuration()

    db: DatabaseContainer = providers.Container(DatabaseContainer, config=config)
    security: SecurityContainer = providers.Container(SecurityContainer, config=config)
    interactors: InteractorsContainer = providers.Container(
        InteractorsContainer,
        password_hasher=security.password_hasher,
        token_service=security.token_service,
        signature_service=security.signature_service,
    )
    mappers: MappersContainer = providers.Container(MappersContainer)


def build_container() -> Container:
    """Build and configure the DI container from settings."""
    container = Container()
    container.config.from_pydantic(settings)
    return container
