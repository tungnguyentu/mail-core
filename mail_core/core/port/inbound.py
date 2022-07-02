from typing import Protocol

from mail_core.models.mail import (
    DeactivateMailPayload,
    DeactivateMailResponse,
    MailCreateFreeCommand,
    MailDeletePayload,
    MailDeleteResponse,
    MailGetQuotaCommand,
    MailGetQuotaResponse,
    MailRefillCommand,
    MailExpireCommand,
    CreateQuotaCommand,
    UpdateQuotaCommand,
    MailCreatePayload,
    MailRefillPayload,
    CreateQuotaPayload,
    UpdateQuotaPayload,
    QuotaModel,
    MailCreateFreeResponse,
    MailRefillResponse,
    MailExpireResponse,
    MailCreateQuotaResponse,
    MailUpdateQuotaResponse
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
    
    def activate_email(self, command):
        ...
    
    def delete_email(self, command: MailDeletePayload) -> MailDeleteResponse:
        ...
    
    def create_account_quota(self, command: CreateQuotaPayload) -> MailCreateQuotaResponse:
        ...
    
    def update_account_quota(self, command: UpdateQuotaPayload) -> MailUpdateQuotaResponse:
        ...

    def get_quota(self, command: MailGetQuotaCommand) -> MailGetQuotaResponse:
        ...