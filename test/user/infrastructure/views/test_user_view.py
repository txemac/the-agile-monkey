from datetime import datetime
from http import HTTPStatus
from typing import Dict

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

import messages
from user.domain.user import User
from user.domain.user import UserUpdate
from user.domain.user_repository import UserRepository
from utils import assert_dicts
from utils import assert_lists


def test_user_create_ok(
        client: TestClient,
        user_admin_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
) -> None:
    count_1 = user_repository.count(db_session)
    data = dict(
        username="monkey",
        password="password",
        is_admin=False,
    )
    response = client.post(
        url="/users",
        json=data,
        headers=user_admin_headers,
    )
    assert response.status_code == HTTPStatus.CREATED
    count_2 = user_repository.count(db_session)
    assert count_1 + 1 == count_2


def test_user_create_username_already_exists(
        client: TestClient,
        user_admin_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_1: User,
) -> None:
    data = dict(
        username=user_1.username,
        password="password",
        is_admin=False,
    )
    response = client.post(
        url="/users",
        json=data,
        headers=user_admin_headers,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == messages.USERNAME_ALREADY_EXISTS


def test_user_create_without_permissions(
        client: TestClient,
        user_1_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
) -> None:
    data = dict(
        username="monkey",
        password="password",
        is_admin=False,
    )
    response = client.post(
        url="/users",
        json=data,
        headers=user_1_headers,
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()["detail"] == messages.USER_NOT_PERMISSION


def test_user_get_list_only_users(
        client: TestClient,
        user_admin_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_1: User,
) -> None:
    response = client.get(
        url="/users",
        headers=user_admin_headers,
    )
    assert response.status_code == HTTPStatus.OK
    expected = [user_1.dict(exclude={"password"})]
    assert_lists(original=response.json(), expected=expected)


def test_user_get_list_only_actives(
        client: TestClient,
        user_admin_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_admin: User,
        user_1: User,
) -> None:
    user_repository.update(db_session, user_id=user_1.id, new_info=UserUpdate(dt_deleted=datetime.utcnow()))
    response = client.get(
        url="/users?only_users=false&only_actives=true",
        headers=user_admin_headers,
    )
    assert response.status_code == HTTPStatus.OK
    expected = [user_admin.dict(exclude={"password"})]
    assert_lists(original=response.json(), expected=expected)


def test_user_get_list_all(
        client: TestClient,
        user_admin_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_admin: User,
        user_1: User,
) -> None:
    response = client.get(
        url="/users?only_users=false",
        headers=user_admin_headers,
    )
    assert response.status_code == HTTPStatus.OK
    expected = [user_admin.dict(exclude={"password"}), user_1.dict(exclude={"password"})]
    assert_lists(original=response.json(), expected=expected)


def test_user_get_list_without_permissions(
        client: TestClient,
        user_1_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_1: User,
) -> None:
    response = client.get(
        url="/users",
        headers=user_1_headers,
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()["detail"] == messages.USER_NOT_PERMISSION


def test_user_update_ok(
        client: TestClient,
        user_admin_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_1: User,
) -> None:
    count_1 = user_repository.count(db_session)
    data = dict(
        username="new_username",
        password="new_password",
        is_admin=True,
        dt_deleted="2021-11-11T12:34:56",
    )
    response = client.patch(
        url=f"/users/{user_1.id}",
        json=data,
        headers=user_admin_headers,
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
    count_2 = user_repository.count(db_session)
    assert count_1 == count_2

    user_db = user_repository.get_by_id(db_session, user_id=user_1.id)
    data["id"] = str(user_1.id)
    data["dt_created"] = user_1.dt_created
    data["password"] = "*"
    assert_dicts(original=user_db.__dict__, expected=data)


def test_user_update_without_permissions(
        client: TestClient,
        user_1_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_1: User,
) -> None:
    response = client.patch(
        url=f"/users/{user_1.id}",
        json=dict(),
        headers=user_1_headers,
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()["detail"] == messages.USER_NOT_PERMISSION
