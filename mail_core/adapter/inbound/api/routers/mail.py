from fastapi import APIRouter, Depends

from mail_core.core.port.inbound import MailCreateUseCase
from mail_core.adapter.inbound.api.dependencies.mail import create_email_service

router = APIRouter()


@router.post("/create")
def create(service: MailCreateUseCase = Depends(create_email_service)):
    resposne = service.create_random_email_address()
    return resposne
