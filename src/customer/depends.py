from http import HTTPStatus

from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

import messages
from customer.domain.customer import Customer
from customer.domain.customer_repository import CustomerRepository
from database import get_db
from dependency_injection import di_customer_repository


def get_customer_by_id(
        *,
        db_session: Session = Depends(get_db),
        customer_repository: CustomerRepository = Depends(di_customer_repository),
        customer_id: str,
) -> Customer:
    """
    Get customer by customer_id.

    :param db_session: session of the database
    :param customer_repository: customer repository
    :param customer_id: customer's ID
    :raise: HTTPException if customer not exists
    :return: user
    """
    customer_db = customer_repository.get_by_id(db_session=db_session, customer_id=customer_id)

    if customer_db is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.CUSTOMER_NOT_FOUND)

    return customer_db
