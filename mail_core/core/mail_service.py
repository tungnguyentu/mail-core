import crypt
import string
from random import shuffle, choice
from datetime import datetime

from mail_core.core.port.outbound import MailCoreRepository
from mail_core.models.mail import MailCreatePayload, MailCreateResponse


class MailService:
    def __init__(self, repository: MailCoreRepository):
        self.repo = repository

    def create_random_email_address(self) -> MailCreateResponse:
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
        payload = MailCreatePayload(
            email=email_address,
            password=password,
            init_at=init_at,
            expire=expire,
            domain_id=domain.domain_id,
        )
        response = self.repo.create_email(payload)
        return MailCreateResponse(email=response.email, expire=response.expire)

    # def refill(self, email: str) -> None:
    #     current_time = int(datetime.now().timestamp())
    #     default_interval = Settings.DEFAULT_INTERVAL
    #     expire = self.repo.get_expire(email)
    #     if expire is None:
    #         expire = current_time + default_interval
    #     else:
    #         expire = expire + (default_interval - (expire - current_time))
    #     self.repo.set_expire(email, expire)
    #     return expire
