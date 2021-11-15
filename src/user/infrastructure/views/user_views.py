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
from database import get_db
from depends import check_authenticated_is_admin
from depends import get_user_repository
from main_schema import SchemaID
from user.depends import get_user_by_id
from user.domain.user import User
from user.domain.user import UserCreate
from user.domain.user import UserOut
from user.domain.user import UserUpdate
from user.domain.user_repository import UserRepository

api_users = APIRouter()

logger = logging.getLogger(__name__)


@api_users.post(
    path="",
    description="Create a new user. Only for admins.",
    status_code=HTTPStatus.CREATED,
    response_model=SchemaID,
    responses={
        400: {"description": messages.USERNAME_ALREADY_EXISTS},
        401: {"description": messages.USER_NOT_CREDENTIALS},
        403: {"description": messages.USER_NOT_PERMISSION},
    },
    dependencies=[Depends(check_authenticated_is_admin)],
)
def create(
        *,
        db_session: Session = Depends(get_db),
        user_repository: UserRepository = Depends(get_user_repository),
        payload: UserCreate,
) -> SchemaID:
    # check the unique username
    user_db = user_repository.get_by_username(db_session=db_session, username=payload.username)
    if user_db:
        logger.exception(messages.USERNAME_ALREADY_EXISTS)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=messages.USERNAME_ALREADY_EXISTS)

    # create new user
    new_user = user_repository.create(db_session=db_session, user=payload)
    if not new_user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=messages.USER_CREATE_ERROR)

    return SchemaID(id=new_user.id)


@api_users.get(
    path="",
    description="List all users. Only for admins.",
    response_model=Page[UserOut],
    status_code=HTTPStatus.OK,
    responses={
        400: {"description": messages.USERNAME_ALREADY_EXISTS},
        401: {"description": messages.USER_NOT_CREDENTIALS},
        403: {"description": messages.USER_NOT_PERMISSION},
    },
    dependencies=[Depends(check_authenticated_is_admin)],
)
def get_list(
        *,
        db_session: Session = Depends(get_db),
        user_repository: UserRepository = Depends(get_user_repository),
        params: Params = Depends(),
        only_users: Optional[bool] = True,
        only_actives: Optional[bool] = True,
) -> Page[UserOut]:
    users = user_repository.get_list(db_session, only_users=only_users, only_actives=only_actives)
    return paginate(users, params)


@api_users.patch(
    path="/{uuid}",
    description="Update user. Only for admins.",
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        400: {"description": messages.UUID_NOT_VALID},
        401: {"description": messages.USER_NOT_CREDENTIALS},
        403: {"description": messages.USER_NOT_PERMISSION},
        404: {"description": messages.USER_NOT_FOUND},
    },
    dependencies=[Depends(check_authenticated_is_admin)],
)
def update(
        *,
        db_session: Session = Depends(get_db),
        user_repository: UserRepository = Depends(get_user_repository),
        user: User = Depends(get_user_by_id),
        payload: UserUpdate,
) -> None:
    user_repository.update(db_session, user_id=user.id, new_info=payload)
    return Response(status_code=HTTPStatus.NO_CONTENT.value)


@api_users.delete(
    path="/{uuid}",
    description="Deactivate user. Only for admins.",
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        400: {"description": messages.UUID_NOT_VALID},
        401: {"description": messages.USER_NOT_CREDENTIALS},
        403: {"description": messages.USER_NOT_PERMISSION},
        404: {"description": messages.USER_NOT_FOUND},
    },
    dependencies=[Depends(check_authenticated_is_admin)],
)
def delete(
        *,
        db_session: Session = Depends(get_db),
        user_repository: UserRepository = Depends(get_user_repository),
        user: User = Depends(get_user_by_id),
) -> None:
    user_repository.update(db_session, user_id=user.id, new_info=UserUpdate(dt_deleted=datetime.utcnow()))
    return Response(status_code=HTTPStatus.NO_CONTENT.value)
