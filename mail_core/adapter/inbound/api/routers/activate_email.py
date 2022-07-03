from fastapi import APIRouter, Depends

from mail_core.core.port.inbound import MailUseCase
from mail_core.adapter.inbound.api.dto.mail import ActivateEmailDTO
from mail_core.adapter.inbound.api.dependencies.mail import deactivate_email_service
from mail_core.models.mail import ActivateEmailCommand, ActivateEmailResponse

router = APIRouter()


@router.post("/activate",
    response_model_exclude_unset=True,
    response_model=ActivateEmailResponse,
    tags=["Email"]
)
def activate_email(
    payload: ActivateEmailDTO,
    service: MailUseCase = Depends(deactivate_email_service),
):
    command = ActivateEmailCommand(account_id=payload.account_id, email=payload.email)
    response = service.activate_email(command)
    if not response.status:
        response.status = 404
    else:
        response.status = 200
    return response
