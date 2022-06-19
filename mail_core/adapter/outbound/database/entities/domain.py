from sqlalchemy import Column, String, Integer

from mail_core.adapter.outbound.database.session import Base


class VirtualDomain(Base):
    __tablename__ = "virtual_domains"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False, default="free", index=True)
