import uuid
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy_utils import UUIDType

from database import Base


class SQLAlchemyUser(Base):
    __tablename__ = "user"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, index=True, unique=True)
    password = Column(String, nullable=False)
    dt_created = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    dt_deleted = Column(DateTime(timezone=True), nullable=True)
    is_admin = Column(Boolean, nullable=False)

    def __str__(self) -> str:
        return self.username
