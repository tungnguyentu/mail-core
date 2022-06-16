from fastapi import Depends
from config.environment import Settings
from mail_core.adapter.outbound.database.mail_adapter import MysqlAdapter
from mail_core.core.mail_service import MailService
from mail_core.adapter.outbound.database.session import get_db


def mail_core_repositry(session=Depends(get_db), settings=Depends(Settings)):
    return MysqlAdapter(session, settings)


def create_email_service(repo=Depends(mail_core_repositry)) -> MailService:
    return MailService(repo)
