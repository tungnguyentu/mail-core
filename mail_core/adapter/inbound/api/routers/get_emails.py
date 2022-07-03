from fastapi import APIRouter, Depends

from mail_core.core.port.inbound import MailUseCase
from mail_core.adapter.inbound.api.dto.mail import GetEmailsDTO
from mail_core.adapter.inbound.api.dependencies.mail import get_emails_service
from mail_core.models.mail import GetEmailsCommand, GetEmailsResponse

router = APIRouter()


@router.get(
    "/emails",
    response_model_exclude_unset=True,
    response_model=GetEmailsResponse,
    tags=["Email"]
)
def get_emails(
    payload: GetEmailsDTO = Depends(GetEmailsDTO),
    service: MailUseCase = Depends(get_emails_service),
):
    command = GetEmailsCommand(account_id=payload.account_id)
    response = service.get_emails(command)
    if not response.status:
        response.status = 404
    else:
        response.status = 200
    return response
