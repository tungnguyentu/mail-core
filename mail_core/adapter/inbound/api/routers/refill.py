from fastapi import APIRouter, Depends

from mail_core.adapter.inbound.api.dto.mail import RefillDTO
from mail_core.core.port.inbound import MailUseCase
from mail_core.models.mail import MailRefillCommand, MailRefillResponse
from mail_core.adapter.inbound.api.dependencies.mail import (
    refill_email_service,
)

router = APIRouter()


@router.post("/refill", response_model_exclude_unset=True, response_model=MailRefillResponse)
def refill(
    payload: RefillDTO, service: MailUseCase = Depends(refill_email_service)
):
    command = MailRefillCommand(email=payload.email, account_id=payload.account_id)
    response = service.refill(command)
    if not response.status:
        response.status = 404
    else:
        response.status = 200
    return response
