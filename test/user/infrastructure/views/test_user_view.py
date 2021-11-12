from http import HTTPStatus
from typing import Dict

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

import messages
from user.domain.user import User
from user.domain.user_repository import UserRepository


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
