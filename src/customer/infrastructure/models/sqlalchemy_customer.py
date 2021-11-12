from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String

from database import Base


class SQLAlchemyCustomer(Base):
    __tablename__ = "customer"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)
    dt_created = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    dt_deleted = Column(DateTime(timezone=True), nullable=True)

    def __str__(self) -> str:
        return self.id
