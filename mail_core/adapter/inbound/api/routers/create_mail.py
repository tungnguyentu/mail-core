from fastapi import APIRouter, Depends

from mail_core.adapter.inbound.api.dto.mail import CreateFreeEmailDTO
from mail_core.core.port.inbound import MailUseCase
from mail_core.adapter.inbound.api.dependencies.mail import (
    create_email_service,
)
from mail_core.models.mail import MailCreateResponse

router = APIRouter()


@router.post(
    "/free-email",
    response_model_exclude_unset=True,
    response_model=MailCreateResponse,
)
def create(
    payload: CreateFreeEmailDTO,
    service: MailUseCase = Depends(create_email_service),
):
    return service.create_random_email_address(payload)
