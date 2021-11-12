from http import HTTPStatus

from starlette.testclient import TestClient

import messages
from user.domain.user import User
from user.security import create_access_token
from utils import assert_dicts


def test_generate_token_ok(
        client: TestClient,
        user_1: User,
) -> None:
    data = dict(
        username=user_1.username,
        password="password",
    )
    response = client.post(
        url="/auth/token",
        json=data,
    )
    assert response.status_code == HTTPStatus.OK
    expected = dict(
        access_token=create_access_token(username=user_1.username),
        token_type="bearer",
    )
    assert_dicts(original=response.json(), expected=expected)


def test_generate_token_customer_not_exists(
        client: TestClient,
) -> None:
    data = dict(
        username="not_exists",
        password="test",
    )
    response = client.post(
        url="/auth/token",
        json=data,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == messages.USER_NOT_FOUND


def test_generate_token_password_not_correct(
        client: TestClient,
        user_1: User,
) -> None:
    data = dict(
        username=user_1.username,
        password='wrong_password',
    )
    response = client.post(
        url="/auth/token",
        json=data,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == messages.USER_INCORRECT_USERNAME_PASSWORD
