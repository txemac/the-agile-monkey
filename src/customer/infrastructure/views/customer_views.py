from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

import messages
from customer.depends import get_customer_by_id
from customer.domain.customer import Customer
from customer.domain.customer import CustomerCreate
from customer.domain.customer_repository import CustomerRepository
from database import get_db
from dependency_injection import di_customer_repository

api_customers = APIRouter()


@api_customers.post(
    path="",
    description="Create a new customer.",
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.BAD_REQUEST: {"description": messages.CUSTOMER_ID_ALREADY_EXISTS},
        HTTPStatus.UNAUTHORIZED: {"description": messages.USER_NOT_CREDENTIALS},
        HTTPStatus.FORBIDDEN: {"description": messages.USER_NOT_PERMISSION},
    },
)
def create(
        *,
        db_session: Session = Depends(get_db),
        customer_repository: CustomerRepository = Depends(di_customer_repository),
        payload: CustomerCreate,
) -> None:
    # check the unique id
    customer_db = customer_repository.get_by_id(db_session=db_session, customer_id=payload.id)
    if customer_db:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=messages.CUSTOMER_ID_ALREADY_EXISTS)

    # create new customer
    new_customer = Customer(
        dt_created=datetime.utcnow(),
        **payload.dict(),
    )
    created = customer_repository.create(db_session=db_session, customer=new_customer)
    if not created:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=messages.CUSTOMER_CREATE_ERROR)


@api_customers.get(
    path="/{customer_id}",
    description="Get all info about a customer.",
    response_model=Customer,
    status_code=HTTPStatus.OK,
    responses={
        HTTPStatus.UNAUTHORIZED: {"description": messages.USER_NOT_CREDENTIALS},
        HTTPStatus.FORBIDDEN: {"description": messages.USER_NOT_PERMISSION},
        HTTPStatus.NOT_FOUND: {"description": messages.CUSTOMER_NOT_FOUND},
    },
)
def get_one(
        *,
        customer_db: Customer = Depends(get_customer_by_id),
) -> Customer:
    return customer_db
