import logging
from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

import messages
import settings
from customer.domain.customer import Customer
from customer.domain.customer_repository import CustomerRepository
from customer.domain.image_storage_service import ImageStorageService
from customer.infrastructure.repositories.sqlalchemy_customer_repository import SQLAlchemyCustomerRepository
from customer.infrastructure.services.aws_s3_image_storage_service import AWSS3ImageStorageService
from database import get_db
from user.domain.auth import AuthTokenPayload
from user.domain.user import User
from user.domain.user_repository import UserRepository
from user.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository

logger = logging.getLogger(__name__)


def get_user_repository() -> UserRepository:
    return SQLAlchemyUserRepository()


def get_customer_repository() -> CustomerRepository:
    return SQLAlchemyCustomerRepository()


def get_image_storage_service() -> ImageStorageService:
    return AWSS3ImageStorageService()


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


def str_to_uuid(
        uuid: str,
) -> Optional[UUID]:
    """
    Check is a str is a valid UUID.
    Return UUID or error.

    :param uuid: string
    :return: UUID
    """
    if uuid is None:
        return None
    try:
        result = UUID(str(uuid))
    except ValueError as e:
        logger.exception(str(e))
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=messages.UUID_NOT_VALID)
    return result


def get_current_user(
        db_session: Session = Depends(get_db),
        user_repository: UserRepository = Depends(get_user_repository),
        token: str = Depends(reusable_oauth2),
) -> User:
    """
    Get current user.

    :param db_session: database session
    :param user_repository: user repository
    :param token: user's ID
    :return: user
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        token_data = AuthTokenPayload(**payload)
    except (JWTError, ValidationError) as e:
        logger.exception(str(e))
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=messages.USER_NOT_CREDENTIALS)

    user_db = user_repository.get_by_username(db_session=db_session, username=token_data.sub)
    if not user_db or user_db.dt_deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.USER_NOT_FOUND)

    return user_db


def check_authenticated(
        current_user: User = Depends(get_current_user)
) -> None:
    """
    Return error if the current user is NOT admin.

    :param current_user: current user
    """
    if not current_user:
        logger.exception(messages.USER_NOT_PERMISSION)
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=messages.USER_NOT_PERMISSION)


def check_authenticated_is_admin(
        current_user: User = Depends(get_current_user)
) -> None:
    """
    Return error if the current user is NOT admin.

    :param current_user: current user
    """
    if not current_user.is_admin:
        logger.exception(messages.USER_NOT_PERMISSION)
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=messages.USER_NOT_PERMISSION)


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
