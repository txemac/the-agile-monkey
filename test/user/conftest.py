from datetime import datetime
from typing import Dict
from uuid import UUID

import pytest
from sqlalchemy.orm import Session

from user.domain.user import User
from user.domain.user_repository import UserRepository
from user.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from user.security import create_access_token


@pytest.fixture
def user_repository() -> UserRepository:
    return SQLAlchemyUserRepository()


@pytest.fixture
def user_admin(
        db_session: Session,
        user_repository: UserRepository,
) -> User:
    user_admin = User(
        id=UUID("3e0cd031-fb4d-4e8b-942c-cb0633911553"),
        username="user_admin",
        password="password",
        dt_created=datetime.utcnow(),
        is_admin=True,
    )
    user_repository.create(db_session, user=user_admin)
    return user_admin


@pytest.fixture
def user_1(
        db_session: Session,
        user_repository: UserRepository,
) -> User:
    user_1 = User(
        id=UUID("f05acf11-ef44-4e9c-95ea-7699f5fe2d34"),
        username="user_1",
        password="password",
        dt_created=datetime.utcnow(),
        is_admin=False,
    )
    user_repository.create(db_session, user=user_1)
    return user_1


@pytest.fixture
def user_admin_headers(
        user_admin: User,
) -> Dict[str, str]:
    return dict(Authorization=f"Bearer {create_access_token(username=user_admin.username)}")


@pytest.fixture
def user_1_headers(
        user_1: User,
) -> Dict[str, str]:
    return dict(Authorization=f"Bearer {create_access_token(username=user_1.username)}")
