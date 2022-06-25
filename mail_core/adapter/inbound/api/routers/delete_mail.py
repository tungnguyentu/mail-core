from fastapi import APIRouter, Depends

from mail_core.adapter.inbound.api.dto.mail import DeleteMailDTO
from mail_core.core.port.inbound import MailUseCase
from mail_core.adapter.inbound.api.dependencies.mail import (
    delete_email_service
)
from mail_core.models.mail import MailDeleteResponse

router = APIRouter()


@router.delete(
    "/delete",
    response_model_exclude_unset=True,
    response_model=MailDeleteResponse,
)
def delete(
    payload: DeleteMailDTO,
    service: MailUseCase = Depends(delete_email_service),
):
    return service.delete_email(payload)
