from http import HTTPStatus

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

import messages
import settings
from database import get_db
from dependency_injection import di_user_repository
from user.domain.auth import AuthTokenPayload
from user.domain.user import User
from user.domain.user_repository import UserRepository

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_user(
        *,
        db_session: Session = Depends(get_db),
        user_repository: UserRepository = Depends(di_user_repository),
        username: str,
) -> User:
    """
    Get user by username.

    :param db_session: session of the database
    :param user_repository: user repository
    :param username: username
    :raise: HTTPException if user not exists
    :return: user
    """
    user_db = user_repository.get_by_username(db_session=db_session, username=username)

    if user_db is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.USER_NOT_FOUND)

    return user_db


def get_current_user(
        db_session: Session = Depends(get_db),
        user_repository: UserRepository = Depends(di_user_repository),
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
    except (JWTError, ValidationError):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=messages.USER_NOT_CREDENTIALS)

    user_db = user_repository.get_by_username(db_session=db_session, username=token_data.sub)
    if not user_db or not user_db.dt_deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.USER_NOT_FOUND)

    return user_db


def user_admin_permissions(
        current_user: User = Depends(get_current_user)
) -> None:
    """
    Return error if the current user is NOT admin.

    :param current_user: current user
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=messages.USER_NOT_PERMISSION)
