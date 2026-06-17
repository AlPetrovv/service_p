from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from application.dto.auth import LoginDTO
from application.interactors.auth import LoginInteractor
from infra.di.ioc import Container
from infra.resources.database.repos import UOW
from presentation.http.v1.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", summary="Authenticate by email/password")
@inject
async def login(
    body: LoginRequest,
    interactor: LoginInteractor = Depends(Provide[Container.interactors.login]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> TokenResponse:
    dto = LoginDTO(email=str(body.email), password=body.password)
    async with uow:
        token = await interactor(dto=dto, uow=uow)
    return TokenResponse(access_token=token)
