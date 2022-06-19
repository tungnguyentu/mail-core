from typing import Protocol
from mail_core.models.mail import MailCreateResponse


class MailUseCase(Protocol):
    def create_random_email_address(self, payload) -> MailCreateResponse:
        ...

    def refill(self):
        ...

    def get_time_remaining(self, payload):
        ...
