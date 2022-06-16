from mail_core.adapter.outbound.database.models import (
    VirtualDomain,
    VirtualUser,
)
from mail_core.models.mail import Domain, MailCreatePayload
from typing import List


class MysqlAdapter:
    def __init__(self, session, settings) -> None:
        self.session = session
        self.settings = settings

    def get_email(self, email: str) -> str:
        user = (
            self.session.query(VirtualUser)
            .filter(VirtualUser.email == email)
            .first()
        )
        if user is None:
            return None
        return user.email

    def get_free_domain_name(self) -> List[Domain]:
        results = self.session.query(VirtualDomain).all()
        return [
            Domain(name=result.name, domain_id=result.id) for result in results
        ]

    def create_email(self, payload: MailCreatePayload) -> str:
        user = VirtualUser(
            email=payload.email,
            domain_id=payload.domain_id,
            password=payload.password,
            init_at=payload.init_at,
            expire=payload.expire,
        )
        self.session.add(user)
        self.session.commit()
        return user

    def get_expire(self, email: str) -> int:
        ...

    def set_expire(self, email: str, expire: int) -> None:
        ...

    def delete_email(self, email: str) -> None:
        ...
