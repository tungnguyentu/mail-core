from fastapi import APIRouter, Depends


from mail_core.core.port.inbound import MailUseCase
from mail_core.adapter.inbound.api.dto.mail import GetExpireDTO
from mail_core.adapter.inbound.api.dependencies.mail import get_expire_service


router = APIRouter()


@router.get("/remaining-time", response_model_exclude_unset=True)
def expire(
    payload: GetExpireDTO = Depends(GetExpireDTO),
    service: MailUseCase = Depends(get_expire_service),
):
    payload = GetExpireDTO(email=payload.email, account_id=payload.account_id)
    return service.get_time_remaining(payload)
