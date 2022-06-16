from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER

from mail_core.adapter.outbound.database.session import Base


class VirtualDomain(Base):
    __tablename__ = "virtual_domains"

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(50), nullable=False)
