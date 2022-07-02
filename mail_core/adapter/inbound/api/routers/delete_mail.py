from fastapi import APIRouter, Depends

from mail_core.adapter.inbound.api.dto.mail import DeleteMailDTO
from mail_core.core.port.inbound import MailUseCase
from mail_core.adapter.inbound.api.dependencies.mail import (
    delete_email_service
)
from mail_core.models.mail import MailDeleteResponse

router = APIRouter()


@router.delete(
    "/email",
    response_model_exclude_unset=True,
    response_model=MailDeleteResponse,
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
