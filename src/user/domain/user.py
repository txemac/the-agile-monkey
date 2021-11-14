from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import constr


class UserCreate(BaseModel):
    username: constr(min_length=1)
    password: constr(min_length=1)
    is_admin: bool = False


class User(UserCreate):
    id: UUID
    dt_created: datetime
    dt_updated: datetime = None
    dt_deleted: datetime = None


class UserOut(BaseModel):
    id: UUID
    username: constr(min_length=1)
    is_admin: bool = False
    dt_created: datetime
    dt_updated: datetime = None
    dt_deleted: datetime = None

    class Config:
        orm_mode = True

        schema_extra = dict(
            example=dict(
                id="f05acf11-ef44-4e9c-95ea-7699f5fe2d34",
                username="monkey",
                password="hashed password",
                dt_created="2021-11-11 12:34:56",
                dt_updated=None,
                dt_deleted=None,
                is_admin=True,
            )
        )


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    dt_deleted: Optional[datetime] = None
