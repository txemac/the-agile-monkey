from datetime import datetime
from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

import messages
from database import get_db
from depends import di_user_repository
from user.application.user_schema import UserCreate
from user.domain.user import User
from user.domain.user_repository import UserRepository

api_users = APIRouter()


@api_users.post(
    path="",
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.BAD_REQUEST: {"description": messages.USERNAME_ALREADY_EXISTS},
    },
)
def create(
        *,
        db_session: Session = Depends(get_db),
        user_repository: UserRepository = Depends(di_user_repository),
        payload: UserCreate,
) -> str:
    new_user = User(
        id=uuid4(),
        dt_created=datetime.utcnow(),
        **payload.dict(),
    )
    created = user_repository.create(db_session=db_session, user=new_user)

    if not created:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=messages.USER_CREATE_ERROR)

    return str(new_user.id)
