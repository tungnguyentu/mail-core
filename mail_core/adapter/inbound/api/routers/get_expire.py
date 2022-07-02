from fastapi import APIRouter, Depends

from mail_core.core.port.inbound import MailUseCase
from mail_core.adapter.inbound.api.dto.mail import GetExpireDTO
from mail_core.adapter.inbound.api.dependencies.mail import get_expire_service
from mail_core.models.mail import MailExpireCommand, MailExpireResponse

router = APIRouter()


@router.get("/remaining-time", response_model_exclude_unset=True, response_model=MailExpireResponse)
def expire(
    payload: GetExpireDTO = Depends(GetExpireDTO),
    service: MailUseCase = Depends(get_expire_service),
):
    command = MailExpireCommand(email=payload.email, account_id=payload.account_id)
    response = service.get_time_remaining(command)
    if not response.status:
        response.status = 404
    else:
        response.status = 200
    return response