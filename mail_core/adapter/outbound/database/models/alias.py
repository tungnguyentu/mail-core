from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from mail_core.adapter.outbound.database.session import Base


class VirtualAliase(Base):
    __tablename__ = "virtual_aliases"

    id = Column(INTEGER(11), primary_key=True)
    domain_id = Column(
        ForeignKey("virtual_domains.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)

    domain = relationship("VirtualDomain")
