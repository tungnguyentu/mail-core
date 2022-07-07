from fastapi import APIRouter, Depends

from mail_core.adapter.inbound.api.dto.mail import DeleteMailDTO, ClearEmailsDTO
from mail_core.core.port.inbound import MailUseCase
from mail_core.adapter.inbound.api.dependencies.mail import (
    delete_email_service,
    clear_emails_service
)
from mail_core.models.mail import ClearEmailsCommand, MailDeleteResponse, ClearEmailsResponse

router = APIRouter()


@router.delete(
    "/emails",
    response_model_exclude_unset=True,
    response_model=MailDeleteResponse,
    tags=["Email"]
)
def delete_email(
    payload: DeleteMailDTO,
    service: MailUseCase = Depends(delete_email_service),
):
    response = service.delete_email(payload)
    if not response.status:
        response.status = 404
    else:
        response.status = 200
    return response


@router.delete(
    "/emails/clear",
    response_model_exclude_unset=True,
    response_model=ClearEmailsResponse,
    tags=["Email"]
)
def clear(
    payload: ClearEmailsDTO,
    service: MailUseCase = Depends(clear_emails_service),
):
    command = ClearEmailsCommand(
        account_id=payload.account_id
    )
    response = service.clear_emails(command)
    if not response.status:
        response.status = 404
    else:
        response.status = 200
    return response
