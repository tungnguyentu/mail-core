import crypt
import string
from random import shuffle, choice
from datetime import datetime

from sqlalchemy import delete

from mail_core.core.port.outbound import MailCoreRepository
from mail_core.models.mail import (
    MailCreatePayload,
    MailCreateResponse,
    MailRefillPayload,
    QuotaModel,
)


class MailService:
    def __init__(self, repository: MailCoreRepository):
        self.repo = repository

    def create_random_email_address(self, payload) -> MailCreateResponse:
        quota = self.repo.get_account_quota(payload)
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
        password = crypt.crypt("1", crypt.mksalt(crypt.METHOD_SHA512))
        init_at = int(datetime.now().timestamp())
        expire = int(datetime.now().timestamp()) + 600
        mail_payload = MailCreatePayload(
            account_id=payload.account_id,
            email=email_address,
            password=password,
            init_at=init_at,
            expire=expire,
            domain_id=domain.domain_id,
        )
        response = self.repo.create_email(mail_payload)
        quota_payload = QuotaModel(
            account_id=payload.account_id, email_limit=quota.email_limit - 1
        )
        self.repo.update_quota_email_limit(quota_payload)
        return MailCreateResponse(
            message="Email created",
            email=response.email,
            expire=response.expire,
        )

    def refill(self, payload: MailRefillPayload):
        current_time = int(datetime.now().timestamp())
        default_interval = self.repo.get_default_interval()
        expire = self.repo.get_expire(payload)
        if not expire:
            expire = current_time + default_interval
        else:
            expire = expire + (default_interval - (expire - current_time))
        self.repo.set_expire(payload)
        return expire

    def get_time_remaining(self, payload) -> int:
        current_time = int(datetime.now().timestamp())
        expire = self.repo.get_expire(payload)
        if not expire:
            return None
        return expire - current_time

    def deactivate_email(self, payload) -> None:
        self.repo.deactivate_email(payload)
