from fastapi import APIRouter, Depends

from mail_core.adapter.inbound.api.dto.mail import CreateQuotaDTO
from mail_core.core.port.inbound import MailUseCase
from mail_core.adapter.inbound.api.dependencies.mail import (
    create_quota_service
)
from mail_core.models.mail import MailCreateQuotaResponse, CreateQuotaCommand

router = APIRouter()


@router.post(
    "/quota",
    response_model_exclude_unset=True,
    response_model=MailCreateQuotaResponse,
    tags=["Quota"]
)
def create_quota(
    payload: CreateQuotaDTO,
    service: MailUseCase = Depends(create_quota_service)
):
    command = CreateQuotaCommand(
        account_id=payload.account_id,
        email_limit=payload.email_limit,
        custom_email_limit=payload.custom_email_limit,
        alias_limit=payload.alias_limit
    )
    response = service.create_account_quota(command)
    if not response.status:
        response.status = 404
    else:
        response.status = 201
    return response
