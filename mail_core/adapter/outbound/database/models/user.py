from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from mail_core.adapter.outbound.database.session import Base


class VirtualUser(Base):
    __tablename__ = "virtual_users"

    id = Column(INTEGER(11), primary_key=True)
    domain_id = Column(
        ForeignKey("virtual_domains.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    password = Column(String(106), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    init_at = Column(INTEGER(11), nullable=False)
    expire = Column(INTEGER(11), nullable=False)

    domain = relationship("VirtualDomain")
