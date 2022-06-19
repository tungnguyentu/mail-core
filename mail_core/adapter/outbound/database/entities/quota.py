from sqlalchemy import Column, String, Integer

from mail_core.adapter.outbound.database.session import Base


class Quota(Base):
    __tablename__ = "quota"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String(50), nullable=False, index=True)
    email_limit = Column(Integer, nullable=False, default=3)
    custom_email_limit = Column(Integer, nullable=False, default=0)
    alias_limit = Column(Integer, nullable=False, default=0)
