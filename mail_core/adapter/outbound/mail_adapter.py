from mail_core.adapter.outbound.database.entities import (
    VirtualDomain,
    VirtualUser,
    Quota,
)
from mail_core.models.mail import DomainModel, MailCreatePayload
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
        if not user:
            return None
        return user.email

    def get_free_domain_name(self) -> List[DomainModel]:
        results = (
            self.session.query(VirtualDomain)
            .filter(VirtualDomain.type == "free")
            .all()
        )
        return [
            DomainModel(name=result.name, domain_id=result.id)
            for result in results
        ]

    def create_email(self, payload: MailCreatePayload) -> str:
        user = VirtualUser(
            account_id=payload.account_id,
            email=payload.email,
            domain_id=payload.domain_id,
            password=payload.password,
            init_at=payload.init_at,
            expire=payload.expire,
        )
        self.session.add(user)
        self.session.commit()
        return user

    def get_account_quota(self, payload):
        quota = (
            self.session.query(Quota)
            .filter(Quota.account_id == payload.account_id)
            .first()
        )
        return quota

    def update_quota_email_limit(self, payload) -> None:
        response = (
            self.session.query(Quota)
            .filter(
                Quota.account_id == payload.account_id,
            )
            .update({"email_limit": payload.email_limit})
        )
        self.session.commit()
        return response

    def get_default_interval(self) -> int:
        return self.settings.default_interval

    def get_expire(self, payload) -> int:
        result = (
            self.session.query(VirtualUser.expire)
            .filter(
                VirtualUser.account_id == payload.account_id,
                VirtualUser.email == payload.email,
            )
            .first()
        )
        if not result:
            return None
        return result.expire

    def set_expire(self, payload) -> None:
        self.session.query(VirtualUser).filter(
            VirtualUser.account_id == payload.account_id,
            VirtualUser.email == payload.email,
        ).update({"expire": payload.expire})
        self.session.commit()

    def delete_email(self, payload) -> None:
        self.session.query(VirtualUser).filter(
            VirtualUser.account_id == payload.account_id,
            VirtualUser.email == payload.email,
        ).delete()
        self.session.commit()

    def deactivate_email(self, payload) -> None:
        self.session.query(VirtualUser).filter(
            VirtualUser.account_id == payload.account_id,
            VirtualUser.email == payload.email,
        ).update({"active": False})
        self.session.commit()
