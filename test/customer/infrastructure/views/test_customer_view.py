from http import HTTPStatus

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

import messages
from customer.domain.customer import Customer
from customer.domain.customer_repository import CustomerRepository


def test_customer_create_ok(
        client: TestClient,
        db_session: Session,
        customer_repository: CustomerRepository,
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
    )
    assert response.status_code == HTTPStatus.CREATED
    count_2 = customer_repository.count(db_session)
    assert count_1 + 1 == count_2


def test_customer_create_id_already_exists(
        client: TestClient,
        db_session: Session,
        customer_repository: CustomerRepository,
        customer_1: Customer,
) -> None:
    data = dict(
        id=customer_1.id,
        name="The agile monkey SL",
        surname="surname",
    )
    response = client.post(
        url="/customers",
        json=data,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == messages.CUSTOMER_ID_ALREADY_EXISTS
