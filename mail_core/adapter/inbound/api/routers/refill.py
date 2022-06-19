from fastapi import APIRouter, Depends

from mail_core.adapter.inbound.api.dto.mail import RefillDTO
from mail_core.core.port.inbound import MailUseCase
from mail_core.models.mail import MailRefillPayload
from mail_core.adapter.inbound.api.dependencies.mail import (
    refill_email_service,
)

router = APIRouter()


@router.post("/refill")
def refill(
    payload: RefillDTO, service: MailUseCase = Depends(refill_email_service)
):
    payload = MailRefillPayload(email=payload.email)
    resposne = service.refill(payload)
    return resposne
