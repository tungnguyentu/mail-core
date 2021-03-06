import crypt
from typing import List
from config.environment import Settings
from mail_core.adapter.outbound.database.entities import (
    VirtualDomain,
    VirtualUser,
    Quota,
)
from mail_core.models.mail import (
    ActivateEmailResponse,
    ClearEmailsPayload,
    ClearEmailsResponse,
    DeactivateMailPayload, 
    DeactivateMailResponse,
    DomainModel,
    GetEmailResponse,
    GetEmailsCommand,
    GetEmailsResponse,
    MailCreatePayload
)


class MysqlAdapter:
    def __init__(self, session, settings: Settings) -> None:
        self.session = session
        self.settings = settings

    def get_email(self, payload) -> str:
        user = (
            self.session.query(VirtualUser)
            .filter(
                VirtualUser.account_id == payload.account_id,
                VirtualUser.email == payload.email,
            )
            .first()
        )
        if not user:
            return None
        return user.email

    def get_encrypt_password(self, payload):
        password = self.settings.DEFAULT_PASSWORD
        if payload.password:
            password = payload.password
        return crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))

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

    def get_premium_domain_name(self):
        result = (
            self.session.query(VirtualDomain)
            .filter(VirtualDomain.type == "premium")
            .first()
        )
        return DomainModel(name=result.name, domain_id=result.id)

    def create_email(self, payload: MailCreatePayload):
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
        if not quota:
            return None
        return quota

    def create_quota(self, payload):
        quota = Quota(
            account_id=payload.account_id,
            email_limit=payload.email_limit,
            custom_email_limit=payload.custom_email_limit,
            alias_limit=payload.alias_limit
        )
        self.session.add(quota)
        self.session.commit()
        return quota

    def update_quota(self, payload):
        query = self.session.query(Quota).filter(
            Quota.account_id == payload.account_id
        )
        data = {}
        if payload.email_limit is not None:
            data.update({"email_limit": payload.email_limit})
        if payload.custom_email_limit is not None:
            data.update({"custom_email_limit": payload.custom_email_limit})
        if payload.alias_limit is not None:
            data.update({"alias_limit": payload.alias_limit})
        query.update(data)
        self.session.commit()

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
        return self.settings.DEFAULT_INTERVAL

    def get_expire(self, payload):
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
        return result

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

    def deactivate_email(self, payload: DeactivateMailPayload) -> DeactivateMailResponse:
        self.session.query(VirtualUser).filter(
            VirtualUser.account_id == payload.account_id,
            VirtualUser.email == payload.email,
        ).update({"active": False})
        self.session.commit()
        return DeactivateMailResponse(
            account_id=payload.account_id,
            email=payload.email,
        )

    def get_account_emails(self, payload):
        results = (
            self.session.query(VirtualUser)
            .filter(
                VirtualUser.account_id == payload.account_id,
            )
            .all()
        )
        if not results:
            return None
        return [
            GetEmailResponse(
                email=result.email,
                expire=result.expire,
                active=result.active,
            )
            for result in results
        ]

    def activate(self, payload) -> ActivateEmailResponse:
        self.session.query(VirtualUser).filter(
            VirtualUser.account_id == payload.account_id,
            VirtualUser.email == payload.email,
        ).update({"active": True})
        self.session.commit()
        return ActivateEmailResponse(
            account_id=payload.account_id,
            email=payload.email,
        )

    def get_email_info(self, payload) -> GetEmailResponse:
        result = (
            self.session.query(VirtualUser)
            .filter(
                VirtualUser.account_id == payload.account_id,
                VirtualUser.email == payload.email,
            )
            .first()
        )
        if not result:
            return None
        return GetEmailResponse(
            email=result.email,
            expire=result.expire,
            active=result.active,
        )
    
    def get_account(self, payload):
        result = (
            self.session.query(VirtualUser)
            .filter(VirtualUser.id == payload.account_id)
            .first()
        )
        if not result:
            return None
        return result
    
    def clear_emails(self, payload: ClearEmailsPayload):
        self.session.query(VirtualUser).filter(
            VirtualUser.account_id == payload.account_id,
        ).delete()
        self.session.commit()
