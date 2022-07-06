from typing import Protocol

from mail_core.models.mail import (
    CreateEmailPremiumResponse,
    DeactivateMailPayload,
    DeactivateMailResponse,
    GetEmailResponse,
    MailCreateFreeCommand,
    MailDeletePayload,
    MailDeleteResponse,
    MailGetQuotaCommand,
    MailGetQuotaResponse,
    MailRefillCommand,
    MailExpireCommand,
    CreateQuotaCommand,
    UpdateQuotaCommand,
    MailCreateFreeResponse,
    MailRefillResponse,
    MailExpireResponse,
    MailCreateQuotaResponse,
    MailUpdateQuotaResponse,
    GetEmailsResponse,
    ActivateEmailResponse,
    ActivateEmailCommand
)


class MailUseCase(Protocol):

    def create_random_email_address(self, command: MailCreateFreeCommand) -> MailCreateFreeResponse:
        ...

    def refill(self, command: MailRefillCommand) -> MailRefillResponse:
        ...

    def get_time_remaining(self, command: MailExpireCommand) -> MailExpireResponse:
        ...

    def deactivate_email(self, command: DeactivateMailPayload) -> DeactivateMailResponse:
        ...

    def activate_email(self, command: ActivateEmailCommand) -> ActivateEmailResponse:
        ...

    def delete_email(self, command: MailDeletePayload) -> MailDeleteResponse:
        ...

    def create_account_quota(self, command: CreateQuotaCommand) -> MailCreateQuotaResponse:
        ...

    def update_account_quota(self, command: UpdateQuotaCommand) -> MailUpdateQuotaResponse:
        ...

    def get_quota(self, command: MailGetQuotaCommand) -> MailGetQuotaResponse:
        ...

    def get_emails(self, command) -> GetEmailsResponse:
        ...
    
    def get_email(self, command) -> GetEmailResponse:
        ...
    
    def create_premium_email(self, command) -> CreateEmailPremiumResponse:
        ...