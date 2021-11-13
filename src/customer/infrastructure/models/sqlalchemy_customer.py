from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from database import Base


class SQLAlchemyCustomer(Base):
    __tablename__ = "customer"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)
    dt_created = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    dt_updated = Column(DateTime(timezone=True), nullable=True)
    dt_deleted = Column(DateTime(timezone=True), nullable=True)
    created_by_id = Column(UUIDType, ForeignKey("user.id"), nullable=False)
    created_by = relationship("SQLAlchemyUser", foreign_keys=[created_by_id])
    updated_by_id = Column(UUIDType, ForeignKey("user.id"), nullable=True)
    updated_by = relationship("SQLAlchemyUser", foreign_keys=[updated_by_id])

    def __str__(self) -> str:
        return self.id
