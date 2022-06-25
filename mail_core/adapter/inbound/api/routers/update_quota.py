from fastapi import APIRouter, Depends

from mail_core.adapter.inbound.api.dto.mail import UpdateQuotaDTO
from mail_core.core.port.inbound import MailUseCase
from mail_core.adapter.inbound.api.dependencies.mail import (
    update_quota_service
)
from mail_core.models.mail import MailUpdateQuotaResponse, UpdateQuotaCommand

router = APIRouter()


@router.post(
    "/update-quota",
    response_model_exclude_unset=True,
    response_model=MailUpdateQuotaResponse,
)
def update_quota(
    payload: UpdateQuotaDTO,
    service: MailUseCase = Depends(update_quota_service),
):
    command = UpdateQuotaCommand(
        account_id=payload.account_id,
        email_limit=payload.email_limit,
        custom_email_limit=payload.custom_email_limit,
        alias_limit=payload.alias_limit
    )
    return service.update_account_quota(command)
