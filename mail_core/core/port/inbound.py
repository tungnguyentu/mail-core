from typing import Protocol
from mail_core.models.mail import MailCreateResponse


class MailCreateUseCase(Protocol):
    
    def create_random_email_address(self) -> MailCreateResponse:
        ...
