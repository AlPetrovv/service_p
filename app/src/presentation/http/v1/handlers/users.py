from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from application.interactors.user import GetMyAccountsInteractor, GetMyPaymentsInteractor
from domain.entities.user import UserEntity
from infra.di.ioc import Container
from infra.resources.database.repos import UOW
from presentation.http.authentication import get_current_user
from presentation.http.v1.mappers.account import AccountApiMapper
from presentation.http.v1.mappers.payment import PaymentApiMapper
from presentation.http.v1.mappers.user import UserApiMapper
from presentation.http.v1.schemas.account import AccountResponse
from presentation.http.v1.schemas.payment import PaymentResponse
from presentation.http.v1.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", summary="Get current user data")
@inject
async def get_me(
    current_user: UserEntity = Depends(get_current_user),
    mapper: UserApiMapper = Depends(Provide[Container.mappers.user_mapper]),
) -> UserResponse:
    return mapper.to_response(current_user)


@router.get("/me/accounts", summary="List current user's accounts and balances")
@inject
async def get_my_accounts(
    current_user: UserEntity = Depends(get_current_user),
    interactor: GetMyAccountsInteractor = Depends(Provide[Container.interactors.my_accounts]),
    mapper: AccountApiMapper = Depends(Provide[Container.mappers.account_mapper]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> list[AccountResponse]:
    async with uow:
        accounts = await interactor(user_id=current_user.id, uow=uow)
    return [mapper.to_response(account) for account in accounts]


@router.get("/me/payments", summary="List current user's payments")
@inject
async def get_my_payments(
    current_user: UserEntity = Depends(get_current_user),
    interactor: GetMyPaymentsInteractor = Depends(Provide[Container.interactors.my_payments]),
    mapper: PaymentApiMapper = Depends(Provide[Container.mappers.payment_mapper]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> list[PaymentResponse]:
    async with uow:
        payments = await interactor(user_id=current_user.id, uow=uow)
    return [mapper.to_response(payment) for payment in payments]
