import string
from random import shuffle, choice
from datetime import datetime


from mail_core.core.port.outbound import MailCoreRepository
from mail_core.models.mail import (
    MailCreateCommand,
    MailRefillCommand,
    MailExpireCommand,
    CreateQuotaCommand,
    UpdateQuotaCommand,
    MailCreatePayload,
    MailRefillPayload,
    CreateQuotaPayload,
    UpdateQuotaPayload,
    QuotaModel,
    MailCreateResponse,
    MailRefillResponse,
    MailExpireResponse,
    MailCreateQuotaResponse,
    MailUpdateQuotaResponse
)


class MailService:
    def __init__(self, repository: MailCoreRepository):
        self.repo = repository

    def create_random_email_address(self, command: MailCreateCommand) -> MailCreateResponse:
        quota = self.repo.get_account_quota(command)
        if quota.email_limit == 0:
            return MailCreateResponse(
                message="You have reached your email limit"
            )
        domains = self.repo.get_free_domain_name()
        if not domains:
            raise Exception("No domains found")
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
        return MailCreateResponse(
            message="Email created",
            email=response.email,
            expire=response.expire,
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
            email=command.email,
            expire=expire
        )

    def get_time_remaining(self, command: MailExpireCommand) -> MailExpireResponse:
        current_time = int(datetime.now().timestamp())
        result = self.repo.get_expire(command)
        if not result.expire:
            return MailExpireResponse(remaining=0)
        expire = result.expire - current_time
        return MailExpireResponse(
            remaining=expire
        )

    def deactivate_email(self, payload) -> None:
        email = self.repo.get_email(payload)
        if not email:
            raise Exception("Couldn't found email address")
        response = self.repo.deactivate_email(payload)
        return response

    def delete_email(self, payload) -> None:
        exist = self.repo.get_email(payload)
        if not exist:
            return Exception("Email not found")
        self.repo.delete_email(payload)

    def create_account_quota(self, command: CreateQuotaCommand) -> MailCreateQuotaResponse:
        quota = self.repo.get_account_quota(command)
        if quota:
            return MailCreateQuotaResponse(
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
            message = "Create Account Quota Success",
            account_id=response.account_id,
            email_limit=response.email_limit,
            custom_email_limit=response.custom_email_limit,
            alias_limit=response.alias_limit
        )

    def update_account_quota(self, command: UpdateQuotaCommand) -> MailUpdateQuotaResponse:
        quota = self.repo.get_account_quota(command)
        if not quota:
            return MailUpdateQuotaResponse(message="Quota not found")
        payload = UpdateQuotaPayload(
            account_id=command.account_id,
            email_limit=command.email_limit,
            custom_email_limit=command.custom_email_limit,
            alias_limit=command.alias_limit
        )
        self.repo.update_quota(payload)
        result = self.repo.get_account_quota(command)
        return MailUpdateQuotaResponse(
            message = "Create Account Quota Success",
            account_id=result.account_id,
            email_limit=result.email_limit,
            custom_email_limit=result.custom_email_limit,
            alias_limit=result.alias_limit
        )