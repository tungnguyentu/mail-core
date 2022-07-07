from fastapi import Depends

from config.environment import Settings

from mail_core.adapter.outbound.mail_adapter import MysqlAdapter
from mail_core.core.mail_service import MailService
from mail_core.adapter.outbound.database.session import get_db


def mail_core_repositry(session=Depends(get_db), settings=Depends(Settings)):
    return MysqlAdapter(session, settings)


def create_email_service(repo=Depends(mail_core_repositry)) -> MailService:
    return MailService(repo)


def refill_email_service(repo=Depends(mail_core_repositry)) -> MailService:
    return MailService(repo)


def get_expire_service(repo=Depends(mail_core_repositry)) -> MailService:
    return MailService(repo)


def delete_email_service(repo=Depends(mail_core_repositry)) -> MailService:
    return MailService(repo)


def create_quota_service(repo=Depends(mail_core_repositry)) -> MailService:
    return MailService(repo)


def update_quota_service(repo=Depends(mail_core_repositry)) -> MailService:
    return MailService(repo)


def get_quota_service(repo=Depends(mail_core_repositry)) -> MailService:
    return MailService(repo)


def get_emails_service(repo=Depends(mail_core_repositry)) -> MailService:
    return MailService(repo)


def deactivate_email_service(repo=Depends(mail_core_repositry)) -> MailService:
    return MailService(repo)


def activate_email_service(repo=Depends(mail_core_repositry)) -> MailService:
    return MailService(repo)


def get_email_service(repo=Depends(mail_core_repositry)) -> MailService:
    return MailService(repo)


def create_premium_email(repo=Depends(mail_core_repositry)) -> MailService:
    return MailService(repo)


def clear_emails_service(repo=Depends(mail_core_repositry)) -> MailService:
    return MailService(repo)
