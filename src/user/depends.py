import logging
from http import HTTPStatus
from uuid import UUID

from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

import messages
from database import get_db
from depends import get_user_repository
from depends import str_to_uuid
from user.domain.user import User
from user.domain.user_repository import UserRepository

logger = logging.getLogger(__name__)


def get_user_by_id(
        *,
        db_session: Session = Depends(get_db),
        user_repository: UserRepository = Depends(get_user_repository),
        user_uuid: UUID = Depends(str_to_uuid),
) -> User:
    """
    Get user by user_id.

    :param db_session: session of the database
    :param user_repository: user repository
    :param user_uuid: user_id str to UUID
    :raise: HTTPException if user not exists
    :return: user
    """
    user_db = user_repository.get_by_id(db_session=db_session, user_id=user_uuid)

    if user_db is None:
        logger.exception(f"{messages.USER_NOT_FOUND} - ID: {user_uuid}")
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.USER_NOT_FOUND)

    return user_db
