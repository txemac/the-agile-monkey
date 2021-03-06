from datetime import datetime
from http import HTTPStatus
from typing import Dict
from uuid import uuid4

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

import messages
from user.domain.user import User
from user.domain.user import UserUpdate
from user.domain.user_repository import UserRepository
from utils import assert_dicts


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
        url="/users?only_users=true",
        headers=user_admin_headers,
    )
    assert response.status_code == HTTPStatus.OK
    items = [user_1.__dict__]
    items[0]["dt_created"] = "*"
    items[0].pop("password")
    expected = dict(
        items=items,
        page=1,
        total=1,
        size=50,
    )
    assert_dicts(original=response.json(), expected=expected)


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
    items = [user_admin.__dict__]
    items[0]["dt_created"] = "*"
    items[0].pop("password")
    expected = dict(
        items=items,
        page=1,
        total=1,
        size=50,
    )
    assert_dicts(original=response.json(), expected=expected)


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
    items = [user_admin.__dict__, user_1.__dict__]
    for item in items:
        item["dt_created"] = "*"
        item.pop("password")
    expected = dict(
        items=items,
        page=1,
        total=2,
        size=50,
    )
    assert_dicts(original=response.json(), expected=expected)


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


def test_user_update_user_id_not_exists(
        client: TestClient,
        user_admin_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_1: User,
) -> None:
    data = dict(
        username="new_username",
        password="new_password",
        is_admin=True,
        dt_deleted="2021-11-11T12:34:56",
    )
    response = client.patch(
        url=f"/users/{uuid4()}",
        json=data,
        headers=user_admin_headers,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == messages.USER_NOT_FOUND


def test_user_update_username_already_exists(
        client: TestClient,
        user_admin_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_admin: User,
        user_1: User,
) -> None:
    data = dict(
        username=user_admin.username,
        password="new_password",
        is_admin=True,
        dt_deleted="2021-11-11T12:34:56",
    )
    response = client.patch(
        url=f"/users/{user_1.id}",
        json=data,
        headers=user_admin_headers,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == messages.USERNAME_ALREADY_EXISTS


def test_user_update_user_id_not_valid(
        client: TestClient,
        user_admin_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_1: User,
) -> None:
    data = dict(
        username="new_username",
        password="new_password",
        is_admin=True,
        dt_deleted="2021-11-11T12:34:56",
    )
    response = client.patch(
        url="/users/not-valid",
        json=data,
        headers=user_admin_headers,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == messages.UUID_NOT_VALID


def test_user_update_myself(
        client: TestClient,
        user_admin_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_admin: User,
) -> None:
    count_1 = user_repository.count(db_session)
    data = dict(
        username="new_username",
        password="new_password",
        is_admin=True,
        dt_deleted="2021-11-11T12:34:56",
    )
    response = client.patch(
        url=f"/users/{user_admin.id}",
        json=data,
        headers=user_admin_headers,
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
    count_2 = user_repository.count(db_session)
    assert count_1 == count_2

    user_db = user_repository.get_by_id(db_session, user_id=user_admin.id)
    data["id"] = str(user_admin.id)
    data["dt_created"] = user_admin.dt_created
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


def test_user_delete_ok(
        client: TestClient,
        user_admin_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_1: User,
) -> None:
    count_1 = user_repository.count(db_session)
    response = client.delete(
        url=f"/users/{user_1.id}",
        headers=user_admin_headers,
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
    count_2 = user_repository.count(db_session)
    assert count_1 == count_2

    user_db = user_repository.get_by_id(db_session, user_id=user_1.id)
    assert user_db.dt_deleted is not None


def test_user_delete_user_id_not_exists(
        client: TestClient,
        user_admin_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_1: User,
) -> None:
    response = client.delete(
        url=f"/users/{uuid4()}",
        headers=user_admin_headers,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == messages.USER_NOT_FOUND


def test_user_delete_user_id_not_valid(
        client: TestClient,
        user_admin_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_1: User,
) -> None:
    response = client.delete(
        url="/users/not-valid",
        headers=user_admin_headers,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == messages.UUID_NOT_VALID


def test_user_delete_myself(
        client: TestClient,
        user_admin_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_admin: User,
) -> None:
    count_1 = user_repository.count(db_session)
    response = client.delete(
        url=f"/users/{user_admin.id}",
        headers=user_admin_headers,
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
    count_2 = user_repository.count(db_session)
    assert count_1 == count_2

    user_db = user_repository.get_by_id(db_session, user_id=user_admin.id)
    assert user_db.dt_deleted is not None


def test_user_delete_without_permissions(
        client: TestClient,
        user_1_headers: Dict,
        db_session: Session,
        user_repository: UserRepository,
        user_1: User,
) -> None:
    response = client.delete(
        url=f"/users/{user_1.id}",
        headers=user_1_headers,
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()["detail"] == messages.USER_NOT_PERMISSION
