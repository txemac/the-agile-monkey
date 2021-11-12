from datetime import datetime
from http import HTTPStatus
from typing import List
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

import messages
from database import get_db
from dependency_injection import di_user_repository
from main_schema import SchemaID
from user.depends import check_current_user_is_admin
from user.domain.user import User
from user.domain.user import UserCreate
from user.domain.user_repository import UserRepository

api_users = APIRouter()


@api_users.post(
    path="",
    description="Create a new user. Only for admins.",
    status_code=HTTPStatus.CREATED,
    response_model=SchemaID,
    responses={
        HTTPStatus.BAD_REQUEST: {"description": messages.USERNAME_ALREADY_EXISTS},
        HTTPStatus.UNAUTHORIZED: {"description": messages.USER_NOT_CREDENTIALS},
        HTTPStatus.FORBIDDEN: {"description": messages.USER_NOT_PERMISSION},
    },
    dependencies=[Depends(check_current_user_is_admin)],
)
def create(
        *,
        db_session: Session = Depends(get_db),
        user_repository: UserRepository = Depends(di_user_repository),
        payload: UserCreate,
) -> SchemaID:
    # check the unique username
    user_db = user_repository.get_by_username(db_session=db_session, username=payload.username)
    if user_db:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=messages.USERNAME_ALREADY_EXISTS)

    # create new user
    new_user = User(
        id=uuid4(),
        dt_created=datetime.utcnow(),
        **payload.dict(),
    )
    created = user_repository.create(db_session=db_session, user=new_user)
    if not created:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=messages.USER_CREATE_ERROR)

    return SchemaID(id=new_user.id)


@api_users.get(
    path="",
    description="List all users. Only for admins.",
    response_model=List[User],
    response_model_exclude={"password"},
    status_code=HTTPStatus.OK,
    responses={
        HTTPStatus.BAD_REQUEST: {"description": messages.USERNAME_ALREADY_EXISTS},
        HTTPStatus.UNAUTHORIZED: {"description": messages.USER_NOT_CREDENTIALS},
        HTTPStatus.FORBIDDEN: {"description": messages.USER_NOT_PERMISSION},
    },
    dependencies=[Depends(check_current_user_is_admin)],
)
def get_list(
        *,
        db_session: Session = Depends(get_db),
        user_repository: UserRepository = Depends(di_user_repository),
        only_users: Optional[bool] = True,
        only_actives: Optional[bool] = True,
) -> List[User]:
    return user_repository.get_list(
        db_session=db_session,
        only_users=only_users,
        only_actives=only_actives,
    )
