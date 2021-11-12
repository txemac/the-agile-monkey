from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from user.domain.user import User
from user.domain.user_repository import UserRepository
from utils import assert_dicts
from utils import assert_lists


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
    created = user_repository.create(db_session, user=new_user)
    count_2 = user_repository.count(db_session)

    assert created is True
    assert count_1 + 1 == count_2


def test_get_by_username_ok(
        db_session: Session,
        user_repository: UserRepository,
        user_1: User,
) -> None:
    result = user_repository.get_by_username(db_session=db_session, username=user_1.username)
    expected = user_1.dict(exclude={"password"})
    assert_dicts(original=result.__dict__, expected=expected)


def test_get_by_username_not_exists(
        db_session: Session,
        user_repository: UserRepository,
) -> None:
    assert user_repository.get_by_username(db_session=db_session, username="non exists") is None


def test_get_list_empty(
        db_session: Session,
        user_repository: UserRepository,
) -> None:
    assert user_repository.get_list(db_session=db_session) == []


def test_get_list_only_users(
        db_session: Session,
        user_repository: UserRepository,
        user_admin: User,
        user_1: User,
) -> None:
    result = user_repository.get_list(db_session=db_session, only_users=True)
    original = [user.__dict__ for user in result]
    expected = [user_1.dict(exclude={"password"})]
    assert_lists(original=original, expected=expected)


def test_get_list_all(
        db_session: Session,
        user_repository: UserRepository,
        user_admin: User,
        user_1: User,
) -> None:
    result = user_repository.get_list(db_session=db_session, only_users=False)
    original = [user.__dict__ for user in result]
    expected = [user_admin.dict(exclude={"password"}), user_1.dict(exclude={"password"})]
    assert_lists(original=original, expected=expected)
