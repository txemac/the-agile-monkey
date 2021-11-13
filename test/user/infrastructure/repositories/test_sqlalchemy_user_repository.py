from datetime import datetime

from sqlalchemy.orm import Session

from user.domain.user import User
from user.domain.user import UserCreate
from user.domain.user import UserUpdate
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
    new_user = UserCreate(
        username="monkey",
        password="password",
        is_admin=False,
    )
    count_1 = user_repository.count(db_session)
    user = user_repository.create(db_session, user=new_user)
    count_2 = user_repository.count(db_session)

    assert count_1 + 1 == count_2

    user_db = user_repository.get_by_id(db_session, user_id=user.id)
    expected = new_user.dict()
    expected["id"] = "*"
    expected["password"] = "*"
    expected["dt_created"] = "*"
    expected["dt_updated"] = None
    expected["dt_deleted"] = None
    assert_dicts(original=user_db.__dict__, expected=expected)


def test_update_ok(
        db_session: Session,
        user_repository: UserRepository,
        user_1: User,
) -> None:
    new_info = UserUpdate(
        username="new_username",
        password="new_password",
        is_admin=not user_1.is_admin,
        dt_deleted=datetime.utcnow(),
    )
    user_repository.update(db_session, user_id=user_1.id, new_info=new_info)

    user_db = user_repository.get_by_id(db_session, user_id=user_1.id)
    expected = new_info.dict()
    expected["dt_updated"] = "*"
    assert_dicts(original=user_db.__dict__, expected=expected)


def test_get_by_username_ok(
        db_session: Session,
        user_repository: UserRepository,
        user_1: User,
) -> None:
    result = user_repository.get_by_username(db_session=db_session, username=user_1.username)
    expected = user_1.__dict__
    expected.pop("password")
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
    expected = [user_1.__dict__]
    expected[0].pop("password")
    assert_lists(original=original, expected=expected)


def test_get_list_all(
        db_session: Session,
        user_repository: UserRepository,
        user_admin: User,
        user_1: User,
) -> None:
    result = user_repository.get_list(db_session=db_session, only_users=False)
    original = [user.__dict__ for user in result]
    expected = [user_admin.__dict__, user_1.__dict__]
    for element in expected:
        element.pop("password")
    assert_lists(original=original, expected=expected)


def test_get_list_only_actives(
        db_session: Session,
        user_repository: UserRepository,
        user_admin: User,
        user_1: User,
) -> None:
    user_repository.update(
        db_session=db_session,
        user_id=user_1.id,
        new_info=UserUpdate(dt_deleted=datetime.utcnow()),
    )
    result = user_repository.get_list(db_session=db_session, only_users=False, only_actives=True)
    original = [user.__dict__ for user in result]
    expected = [user_admin.__dict__]
    for element in expected:
        element.pop("password")
    assert_lists(original=original, expected=expected)
