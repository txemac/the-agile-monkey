from http import HTTPStatus
from typing import Dict

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

import messages
from customer.domain.customer import Customer
from customer.domain.customer_repository import CustomerRepository
from user.domain.user import User
from utils import assert_dicts


def test_customer_create_ok(
        client: TestClient,
        db_session: Session,
        customer_repository: CustomerRepository,
        user_1_headers: Dict,
        user_1: User,
) -> None:
    count_1 = customer_repository.count(db_session)
    data = dict(
        id="The Agile Monkey",
        name="The agile monkey SL",
        surname="surname",
        photo_url="https://assets.website-files.com/5bea194a3705ec25b27ce94e/5bea1afbc107657eff26fb3d_Logo"
                  "%20the%20agile%20monkeys.svg",
    )
    response = client.post(
        url="/customers",
        json=data,
        headers=user_1_headers,
    )
    assert response.status_code == HTTPStatus.CREATED
    count_2 = customer_repository.count(db_session)
    assert count_1 + 1 == count_2

    customer_db = customer_repository.get_by_id(db_session, customer_id=data["id"])
    data["created_by_id"] = user_1.id
    data["updated_by_id"] = None
    data["dt_created"] = "*"
    data["dt_updated"] = None
    data["dt_deleted"] = None
    assert_dicts(original=customer_db.__dict__, expected=data)


def test_customer_create_id_already_exists(
        client: TestClient,
        db_session: Session,
        customer_repository: CustomerRepository,
        customer_1: Customer,
        user_1_headers: Dict,
) -> None:
    data = dict(
        id=customer_1.id,
        name="The agile monkey SL",
        surname="surname",
    )
    response = client.post(
        url="/customers",
        json=data,
        headers=user_1_headers,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == messages.CUSTOMER_ID_ALREADY_EXISTS


def test_customer_get_one_ok(
        client: TestClient,
        db_session: Session,
        customer_repository: CustomerRepository,
        customer_1: Customer,
        user_1_headers: Dict,
        user_1: User,
) -> None:
    response = client.get(
        url=f"/customers/{customer_1.id}",
        headers=user_1_headers,
    )
    assert response.status_code == HTTPStatus.OK
    assert_dicts(original=response.json(), expected=customer_1.__dict__)


def test_customer_get_one_not_exists(
        client: TestClient,
        db_session: Session,
        customer_repository: CustomerRepository,
        user_1_headers: Dict,
) -> None:
    response = client.get(
        url="/customers/not_exists",
        headers=user_1_headers,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == messages.CUSTOMER_NOT_FOUND


def test_customer_update_ok(
        client: TestClient,
        db_session: Session,
        customer_repository: CustomerRepository,
        customer_1: Customer,
        user_1_headers: Dict,
) -> None:
    count_1 = customer_repository.count(db_session)
    data = dict(
        id="new_customer_id",
        name="new_name",
        surname="new_surname",
        photo_url="new_photo_url",
        dt_deleted="2021-11-11T12:34:56",
    )
    response = client.patch(
        url=f"/customers/{customer_1.id}",
        json=data,
        headers=user_1_headers,
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
    count_2 = customer_repository.count(db_session)
    assert count_1 == count_2

    customer_db = customer_repository.get_by_id(db_session, customer_id=data["id"])
    assert_dicts(original=customer_db.__dict__, expected=data)


def test_customer_update_customer_id_not_exists(
        client: TestClient,
        db_session: Session,
        customer_repository: CustomerRepository,
        customer_1: Customer,
        user_1_headers: Dict,
) -> None:
    data = dict(
        id="new_customer_id",
        name="new_name",
        surname="new_surname",
        photo_url="new_photo_url",
        dt_deleted="2021-11-11T12:34:56",
    )
    response = client.patch(
        url="/customers/non_exists",
        json=data,
        headers=user_1_headers,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == messages.CUSTOMER_NOT_FOUND


def test_customer_delete_ok(
        client: TestClient,
        db_session: Session,
        customer_repository: CustomerRepository,
        customer_1: Customer,
        user_1_headers: Dict,
) -> None:
    count_1 = customer_repository.count(db_session)
    response = client.delete(
        url=f"/customers/{customer_1.id}",
        headers=user_1_headers,
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
    count_2 = customer_repository.count(db_session)
    assert count_1 == count_2

    customer_db = customer_repository.get_by_id(db_session, customer_id=customer_1.id)
    assert customer_db.dt_deleted is not None


def test_customer_delete_customer_id_not_exists(
        client: TestClient,
        db_session: Session,
        customer_repository: CustomerRepository,
        customer_1: Customer,
        user_1_headers: Dict,
) -> None:
    response = client.delete(
        url="/customers/non_exists",
        headers=user_1_headers,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == messages.CUSTOMER_NOT_FOUND
