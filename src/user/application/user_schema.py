from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool = False


class UserDB(UserCreate):
    id: UUID
    dt_created: datetime
    dt_deleted: datetime

    class Config:
        orm_mode = True
