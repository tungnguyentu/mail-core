from fastapi import APIRouter, Depends

from mail_core.core.port.inbound import MailUseCase
from mail_core.adapter.inbound.api.dto.mail import DeactivateEmailDTO
from mail_core.adapter.inbound.api.dependencies.mail import deactivate_email_service
from mail_core.models.mail import DeactivateMailPayload, DeactivateMailResponse

router = APIRouter()


@router.post("/deactivate",
    response_model_exclude_unset=True,
    response_model=DeactivateMailResponse,
    tags=["Email"]
)
def deactivate_email(
    payload: DeactivateEmailDTO,
    service: MailUseCase = Depends(deactivate_email_service),
):
    command = DeactivateMailPayload(account_id=payload.account_id, email=payload.email)
    response = service.deactivate_email(command)
    if not response.status:
        response.status = 404
    else:
        response.status = 200
    return response
