from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import constr


class UserCreate(BaseModel):
    username: constr(min_length=1)
    password: constr(min_length=1)
    is_admin: bool = False


class UserDB(UserCreate):
    id: UUID
    dt_created: datetime
    dt_deleted: datetime

    class Config:
        orm_mode = True
