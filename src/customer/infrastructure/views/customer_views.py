import logging
from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi_pagination import Page
from fastapi_pagination import Params
from fastapi_pagination import paginate
from sqlalchemy.orm import Session

import messages
from customer.depends import get_customer_by_id
from customer.domain.customer import Customer
from customer.domain.customer import CustomerCreate
from customer.domain.customer import CustomerUpdate
from customer.domain.customer_repository import CustomerRepository
from database import get_db
from depends import check_authenticated
from depends import get_current_user
from depends import get_customer_repository
from user.domain.user import User

api_customers = APIRouter()

logger = logging.getLogger(__name__)


@api_customers.post(
    path="",
    description="Create a new customer.",
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.BAD_REQUEST: {"description": messages.CUSTOMER_ID_ALREADY_EXISTS},
        HTTPStatus.UNAUTHORIZED: {"description": messages.USER_NOT_CREDENTIALS},
        HTTPStatus.FORBIDDEN: {"description": messages.USER_NOT_PERMISSION},
    },
    dependencies=[Depends(check_authenticated)],
)
def create(
        *,
        db_session: Session = Depends(get_db),
        customer_repository: CustomerRepository = Depends(get_customer_repository),
        # image_storage_service: ImageStorageService = Depends(get_image_storage_service),
        current_user: User = Depends(get_current_user),
        payload: CustomerCreate,
) -> None:
    # check the unique id
    customer_db = customer_repository.get_by_id(db_session=db_session, customer_id=payload.id)
    if customer_db:
        logger.exception(messages.CUSTOMER_ID_ALREADY_EXISTS)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=messages.CUSTOMER_ID_ALREADY_EXISTS)

    # upload photo
    # if payload.photo is not None:
    #    photo_url = image_storage_service.update(
    #        path=f"customer/{payload.id}/photo.png",
    #        image=payload.photo,
    #    )

    # create new customer
    new_customer = customer_repository.create(db_session=db_session, customer=payload, current_user=current_user)
    if not new_customer:
        logger.exception(messages.CUSTOMER_CREATE_ERROR)
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
    dependencies=[Depends(check_authenticated)],
)
def get_one(
        *,
        customer_db: Customer = Depends(get_customer_by_id),
) -> Customer:
    return customer_db


@api_customers.get(
    path="",
    description="List all customers.",
    response_model=Page[Customer],
    status_code=HTTPStatus.OK,
    responses={
        HTTPStatus.BAD_REQUEST: {"description": messages.USERNAME_ALREADY_EXISTS},
        HTTPStatus.UNAUTHORIZED: {"description": messages.USER_NOT_CREDENTIALS},
        HTTPStatus.FORBIDDEN: {"description": messages.USER_NOT_PERMISSION},
    },
    dependencies=[Depends(check_authenticated)],
)
def get_list(
        *,
        db_session: Session = Depends(get_db),
        customer_repository: CustomerRepository = Depends(get_customer_repository),
        params: Params = Depends(),
        only_actives: Optional[bool] = True,
) -> Page[Customer]:
    customers = customer_repository.get_list(db_session=db_session, only_actives=only_actives)
    return paginate(customers, params)


@api_customers.patch(
    path="/{customer_id}",
    description="Update customer.",
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        HTTPStatus.BAD_REQUEST: {"description": messages.UUID_NOT_VALID},
        HTTPStatus.UNAUTHORIZED: {"description": messages.USER_NOT_CREDENTIALS},
        HTTPStatus.FORBIDDEN: {"description": messages.USER_NOT_PERMISSION},
        HTTPStatus.NOT_FOUND: {"description": messages.CUSTOMER_NOT_FOUND},
    },
    dependencies=[Depends(check_authenticated)],
)
def update(
        *,
        db_session: Session = Depends(get_db),
        customer_repository: CustomerRepository = Depends(get_customer_repository),
        # image_storage_service: ImageStorageService = Depends(get_image_storage_service),
        current_user: User = Depends(get_current_user),
        customer: Customer = Depends(get_customer_by_id),
        payload: CustomerUpdate,
        customer_id: str,
) -> None:
    # upload photo
    # if payload.photo is not None:
    #    photo_url = image_storage_service.update(
    #        path=f"customer/{payload.id}/photo.png",
    #        image=payload.photo,
    #    )

    customer_repository.update(
        db_session=db_session,
        customer_id=customer_id,
        new_info=payload,
        current_user=current_user,
    )
    return Response(status_code=HTTPStatus.NO_CONTENT.value)


@api_customers.delete(
    path="/{customer_id}",
    description="Deactivate a customer.",
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        HTTPStatus.UNAUTHORIZED: {"description": messages.USER_NOT_CREDENTIALS},
        HTTPStatus.FORBIDDEN: {"description": messages.USER_NOT_PERMISSION},
        HTTPStatus.NOT_FOUND: {"description": messages.CUSTOMER_NOT_FOUND},
    },
    dependencies=[Depends(check_authenticated)],
)
def delete(
        *,
        db_session: Session = Depends(get_db),
        customer_repository: CustomerRepository = Depends(get_customer_repository),
        current_user: User = Depends(get_current_user),
        customer: Customer = Depends(get_customer_by_id),
        customer_id: str,
) -> None:
    customer_repository.update(
        db_session=db_session,
        customer_id=customer_id,
        new_info=CustomerUpdate(dt_deleted=datetime.utcnow()),
        current_user=current_user,
    )
    return Response(status_code=HTTPStatus.NO_CONTENT.value)
