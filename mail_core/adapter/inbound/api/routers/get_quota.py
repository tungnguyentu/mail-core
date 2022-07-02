from fastapi import APIRouter, Depends

from mail_core.core.port.inbound import MailUseCase
from mail_core.adapter.inbound.api.dto.mail import GetQuotaDTO
from mail_core.adapter.inbound.api.dependencies.mail import get_quota_service
from mail_core.models.mail import MailGetQuotaResponse, MailGetQuotaCommand


router = APIRouter()

@router.get("/quota", response_model_exclude_unset=True, response_model=MailGetQuotaResponse)
def get_quota(
    payload: GetQuotaDTO = Depends(GetQuotaDTO),
    service: MailUseCase = Depends(get_quota_service),
):
    command = MailGetQuotaCommand(account_id=payload.account_id)
    response = service.get_quota(command)
    if not response.status:
        response.status = 404
    else:
        response.status = 200
    return response
