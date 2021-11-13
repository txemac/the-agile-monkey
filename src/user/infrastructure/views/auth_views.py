from http import HTTPStatus

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

import messages
from database import get_db
from depends import get_user_repository
from user.domain.auth import AuthLogin
from user.domain.auth import AuthToken
from user.domain.user_repository import UserRepository
from user.security import create_access_token
from user.security import verify_password

api_auth = APIRouter()


@api_auth.post(
    path="/token",
    status_code=HTTPStatus.OK,
    response_model=AuthToken,
    responses={
        HTTPStatus.BAD_REQUEST: {"description": messages.USER_INCORRECT_USERNAME_PASSWORD}
    },
)
def generate_token(
        *,
        db_session: Session = Depends(get_db),
        user_repository: UserRepository = Depends(get_user_repository),
        payload: AuthLogin,
) -> AuthToken:
    user_db = user_repository.get_by_username(db_session=db_session, username=payload.username)

    if not user_db or user_db.dt_deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.USER_NOT_FOUND)

    if not verify_password(plain_password=payload.password, hashed_password=user_db.password):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=messages.USER_INCORRECT_USERNAME_PASSWORD)

    return AuthToken(
        access_token=create_access_token(username=user_db.username),
        token_type="bearer",
    )
