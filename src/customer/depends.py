import logging
from http import HTTPStatus

from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

import messages
from customer.domain.customer import Customer
from customer.domain.customer_repository import CustomerRepository
from database import get_db
from depends import get_customer_repository

logger = logging.getLogger(__name__)


def get_customer_by_id(
        *,
        db_session: Session = Depends(get_db),
        customer_repository: CustomerRepository = Depends(get_customer_repository),
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
        logger.exception(f"{messages.CUSTOMER_NOT_FOUND} - ID: {customer_id}")
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.CUSTOMER_NOT_FOUND)

    return customer_db
