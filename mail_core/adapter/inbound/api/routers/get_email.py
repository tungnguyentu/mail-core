from fastapi import APIRouter, Depends

from mail_core.core.port.inbound import MailUseCase
from mail_core.adapter.inbound.api.dto.mail import GetEmailDTO
from mail_core.adapter.inbound.api.dependencies.mail import get_email_service
from mail_core.models.mail import GetEmailCommand, GetEmailResponse

router = APIRouter()


@router.get(
    "/email",
    response_model_exclude_unset=True,
    response_model=GetEmailResponse,
    tags=["Email"]
)
def get_email(
    payload: GetEmailDTO = Depends(GetEmailDTO),
    service: MailUseCase = Depends(get_email_service),
):
    command = GetEmailCommand(email=payload.email, account_id=payload.account_id)
    response = service.get_email(command)
    if not response.status:
        response.status = 404
    else:
        response.status = 200
    return response
