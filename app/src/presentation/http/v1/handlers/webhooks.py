from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from application.dto.webhook import WebhookDTO
from application.interactors.webhook import ProcessWebhookInteractor
from infra.di.ioc import Container
from infra.resources.database.repos import UOW
from presentation.http.v1.schemas.webhook import WebhookRequest, WebhookResponse

router = APIRouter(prefix="/webhook", tags=["Webhook"])


@router.post("/payment", summary="Process a third-party payment webhook")
@inject
async def process_payment_webhook(
    body: WebhookRequest,
    interactor: ProcessWebhookInteractor = Depends(Provide[Container.interactors.process_webhook]),
    uow: UOW = Depends(Provide[Container.db.uow]),
) -> WebhookResponse:
    dto = WebhookDTO(
        transaction_id=body.transaction_id,
        account_id=body.account_id,
        user_id=body.user_id,
        amount=body.amount,
        signature=body.signature,
    )
    async with uow:
        payment = await interactor(dto=dto, uow=uow)
    return WebhookResponse(
        status="ok",
        transaction_id=payment.transaction_id,
        account_id=payment.account_id,
        user_id=payment.user_id,
        amount=payment.amount,
    )
