from datetime import datetime
from uuid import UUID
from uuid import uuid4

from sqlalchemy.orm import Session

from user.domain.user import User
from user.domain.user_repository import UserRepository


def test_count_empty(
    db_session: Session,
    user_repository: UserRepository,
) -> None:
    assert user_repository.count(db_session) == 0


def test_count_ok(
    db_session: Session,
    user_repository: UserRepository,
    user_1: User,
) -> None:
    assert user_repository.count(db_session) == 1


def test_create_ok(
    db_session: Session,
    user_repository: UserRepository,
) -> None:
    new_user = User(
        id=uuid4(),
        username="monkey",
        password="password",
        dt_created=datetime.utcnow(),
        is_admin=False,
    )
    count_1 = user_repository.count(db_session)
    result = user_repository.create(db_session, user=new_user)
    count_2 = user_repository.count(db_session)

    assert isinstance(result, UUID)
    assert count_1 + 1 == count_2
