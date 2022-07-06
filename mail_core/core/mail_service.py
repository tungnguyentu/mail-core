import string
from random import shuffle, choice
from datetime import datetime
from typing import List

from mail_core.utils.logger import logger
from mail_core.core.port.outbound import MailCoreRepository
from mail_core.models.mail import (
    ActivateEmailCommand,
    ActivateEmailResponse,
    CreateEmailPremiumResponse,
    CreateMailPremiumCommand,
    CreateMailPremiumPayload,
    DeactivateMailPayload,
    DeactivateMailResponse,
    GetEmailCommand,
    GetEmailResponse,
    GetEmailsCommand,
    GetEmailsResponse,
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


class MailService:
    def __init__(self, repository: MailCoreRepository):
        self.repo = repository

    def create_random_email_address(self, command: MailCreateFreeCommand) -> MailCreateFreeResponse:
        quota = self.repo.get_account_quota(command)
        if quota.email_limit == 0:
            return MailCreateFreeResponse(
                message="You have reached your email limit",
                status=0
            )
        domains = self.repo.get_free_domain_name()
        if not domains:
            return MailCreateFreeResponse(
                message="No free domains available",
                status=0
            )
        shuffle(domains)
        username = "".join(choice(string.ascii_lowercase) for _ in range(8))
        domain = choice(domains)
        email_address = f"{username}@{domain.name}"
        password = self.repo.get_encrypt_password(command)
        init_at = int(datetime.now().timestamp())
        expire = int(datetime.now().timestamp()) + 600
        payload = MailCreatePayload(
            account_id=command.account_id,
            email=email_address,
            password=password,
            init_at=init_at,
            expire=expire,
            domain_id=domain.domain_id,
        )
        response = self.repo.create_email(payload)
        quota_payload = QuotaModel(
            account_id=command.account_id,
            email_limit=quota.email_limit - 1
        )
        self.repo.update_quota_email_limit(quota_payload)
        logger.info(response)
        return MailCreateFreeResponse(
            message="Create Email Success",
            status=1,
            email=response.email,
            expire=response.expire,
        )

    def create_premium_email(self, command: CreateMailPremiumCommand) -> CreateEmailPremiumResponse:
        quota = self.repo.get_account_quota(command)
        if quota.custom_email_limit == 0:
            return CreateEmailPremiumResponse(
                message="You have reached your email limit",
                status=0
            )
        domain = self.repo.get_premium_domain_name()
        if not domain:
            return MailCreateFreeResponse(
                message="No premium domains available",
                status=0
            )
        email_address = f"{command.username}@{domain.name}"
        password = self.repo.get_encrypt_password(command)
        init_at = int(datetime.now().timestamp())
        payload = MailCreatePayload(
            account_id=command.account_id,
            domain_id=domain.domain_id,
            email=email_address,
            password=password,
            init_at=init_at,
            expire=-1
        )
        response = self.repo.create_email(payload)
        quota_payload = QuotaModel(
            account_id=command.account_id,
            custom_email_limit=quota.custom_email_limit - 1
        )
        self.repo.update_quota(quota_payload)
        return CreateEmailPremiumResponse(
            message="Create Email Success",
            status=1,
            account_id=response.account_id,
            email=response.email
        )

    def refill(self, command: MailRefillCommand) -> MailRefillResponse:
        current_time = int(datetime.now().timestamp())
        default_interval = self.repo.get_default_interval()
        result = self.repo.get_expire(command)
        expire = result.expire
        if not expire:
            expire = current_time + default_interval
        else:
            expire = expire + (default_interval - (expire - current_time))
        payload = MailRefillPayload(
            account_id=command.account_id,
            email=command.email,
            expire=expire
        )
        self.repo.set_expire(payload)
        return MailRefillResponse(
            message="Refill Email Success",
            status=1,
            email=command.email,
            expire=expire
        )

    def get_time_remaining(self, command: MailExpireCommand) -> MailExpireResponse:
        current_time = int(datetime.now().timestamp())
        result = self.repo.get_expire(command)
        if not result.expire:
            return MailExpireResponse(
                message="Expire not found",
                status=0
            )
        expire = result.expire - current_time
        return MailExpireResponse(
            message="Get Time Remaining Success",
            status=1,
            remaining=expire
        )

    def deactivate_email(self, payload: DeactivateMailPayload) -> DeactivateMailResponse:
        email = self.repo.get_email(payload)
        if not email:
            return DeactivateMailResponse(
                message="Email not found",
                status=0
            )
        response = self.repo.deactivate_email(payload)
        return DeactivateMailResponse(
            account_id=response.account_id,
            email=response.email,
            message="Deactivate Email Success",
            status=1
        )

    def delete_email(self, payload: MailDeletePayload) -> MailDeleteResponse:
        exist = self.repo.get_email(payload)
        if not exist:
            return MailDeleteResponse(
                message="Email not found",
                status=0
            )
        self.repo.delete_email(payload)
        email = self.repo.get_email(payload)
        if email:
            return MailDeleteResponse(
                message="Delete Email Failed",
                status=0
            )
        return MailDeleteResponse(
            message="Delete Email Success",
            status=1
        )

    def create_account_quota(self, command: CreateQuotaCommand) -> MailCreateQuotaResponse:
        quota = self.repo.get_account_quota(command)
        if quota:
            return MailCreateQuotaResponse(
                status=0,
                message="The quota for this account already exists"
            )
        payload = CreateQuotaPayload(
            account_id=command.account_id,
            email_limit=command.email_limit,
            custom_email_limit=command.custom_email_limit,
            alias_limit=command.alias_limit
        )
        response = self.repo.create_quota(payload)
        return MailCreateQuotaResponse(
            message="Create Account Quota Success",
            status=1,
            account_id=response.account_id,
            email_limit=response.email_limit,
            custom_email_limit=response.custom_email_limit,
            alias_limit=response.alias_limit
        )

    def update_account_quota(self, command: UpdateQuotaCommand) -> MailUpdateQuotaResponse:
        quota = self.repo.get_account_quota(command)
        if not quota:
            return MailUpdateQuotaResponse(
                message="Quota not found",
                status=0
            )
        payload = UpdateQuotaPayload(
            account_id=command.account_id,
            email_limit=command.email_limit,
            custom_email_limit=command.custom_email_limit,
            alias_limit=command.alias_limit
        )
        self.repo.update_quota(payload)
        result = self.repo.get_account_quota(command)
        return MailUpdateQuotaResponse(
            message="Create Account Quota Success",
            status=1,
            account_id=result.account_id,
            email_limit=result.email_limit,
            custom_email_limit=result.custom_email_limit,
            alias_limit=result.alias_limit
        )

    def get_quota(self, command: MailGetQuotaCommand) -> MailGetQuotaResponse:
        quota = self.repo.get_account_quota(command)
        if not quota:
            return MailGetQuotaResponse(
                message="Quota not found",
                status=0
            )
        return MailGetQuotaResponse(
            message="Get Quota Success",
            status=1,
            account_id=quota.account_id,
            email_limit=quota.email_limit,
            custom_email_limit=quota.custom_email_limit,
            alias_limit=quota.alias_limit
        )

    def get_emails(self, command: GetEmailsCommand) -> GetEmailsResponse:
        emails = self.repo.get_account_emails(command)
        if not emails:
            return GetEmailsResponse(
                message="Emails not found",
                status=0
            )
        return GetEmailsResponse(
            message="Get Emails Success",
            status=1,
            emails=emails
        )

    def activate_email(self, command: ActivateEmailCommand) -> ActivateEmailResponse:
        email = self.repo.get_email(command)
        if not email:
            return ActivateEmailResponse(
                message="Email not found",
                status=0
            )
        response = self.repo.activate(command)
        return ActivateEmailResponse(
            email=response.email,
            message="Activate Email Success",
            status=1
        )

    def get_email(self, command: GetEmailCommand) -> GetEmailResponse:
        email = self.repo.get_email(command)
        if not email:
            return GetEmailResponse(
                message="Email not found",
                status=0
            )
        info = self.repo.get_email_info(command)
        return GetEmailResponse(
            email=info.email,
            expire=info.expire,
            active=info.active,
            message="Get Email Success",
            status=1
        )
