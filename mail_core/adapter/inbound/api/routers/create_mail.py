from fastapi import APIRouter, Depends

from mail_core.adapter.inbound.api.dto.mail import CreateFreeEmailDTO, CreatePremiumEmailDTO
from mail_core.core.port.inbound import MailUseCase
from mail_core.adapter.inbound.api.dependencies.mail import (
    create_email_service,
    create_premium_email
)
from mail_core.models.mail import MailCreateFreeResponse, MailCreateFreeCommand, CreateMailPremiumCommand, CreateEmailPremiumResponse

router = APIRouter()


@router.post(
    "/emails/free",
    response_model_exclude_unset=True,
    response_model=MailCreateFreeResponse,
    tags=["Email"]
)
def create(
    payload: CreateFreeEmailDTO,
    service: MailUseCase = Depends(create_email_service),
):
    command = MailCreateFreeCommand(
        account_id=payload.account_id
    )
    response = service.create_random_email_address(command)
    if not response.status:
        response.status = 404
    else:
        response.status = 201
    return response


@router.post(
    "/emails/premium",
    response_model_exclude_unset=True,
    response_model=CreateEmailPremiumResponse,
    tags=["Email"]
)
def create_premium_email(
    payload: CreatePremiumEmailDTO,
    service: MailUseCase = Depends(create_premium_email),
):
    command = CreateMailPremiumCommand(
        account_id=payload.account_id,
        username=payload.username,
        password=payload.password
    )
    response = service.create_premium_email(command)
    if not response.status:
        response.status = 404
    else:
        response.status = 201
    return response