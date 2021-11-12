from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import constr


class CustomerCreate(BaseModel):
    id: constr(min_length=1)
    name: constr(min_length=1)
    surname: constr(min_length=1)
    photo_url: Optional[str] = None


class Customer(CustomerCreate):
    dt_created: datetime
    dt_deleted: datetime = None

    class Config:
        orm_mode = True

        schema_extra = dict(
            example=dict(
                id="The Agile Monkey",
                name="The agile monkey SL",
                surname="surname",
                photo_url="https://assets.website-files.com/5bea194a3705ec25b27ce94e/5bea1afbc107657eff26fb3d_Logo"
                          "%20the%20agile%20monkeys.svg",
                dt_created="2021-11-11 12:34:56",
                dt_deleted=None,
            )
        )
