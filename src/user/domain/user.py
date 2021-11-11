from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    username: str
    password: str
    dt_created: datetime
    is_admin: bool
    dt_deleted: datetime = None

    def __str__(self) -> str:
        return self.username
