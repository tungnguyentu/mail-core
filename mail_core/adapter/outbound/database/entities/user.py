from sqlalchemy import Boolean, Column, ForeignKey, String, Integer
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from mail_core.adapter.outbound.database.session import Base


class VirtualUser(Base):
    __tablename__ = "virtual_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    domain_id = Column(
        ForeignKey("virtual_domains.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    account_id = Column(String(50), nullable=False, index=True)
    password = Column(String(106), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    init_at = Column(INTEGER(11), nullable=False)
    expire = Column(INTEGER(11), nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    domain = relationship("VirtualDomain")
