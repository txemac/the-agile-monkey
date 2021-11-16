import os
from typing import Any
from typing import Dict
from typing import Generator
from uuid import UUID

import pytest
from alembic.command import downgrade
from alembic.command import upgrade
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from starlette.testclient import TestClient

import settings
from database import get_db
from main import app
from user.domain.user import User
from user.domain.user import UserCreate
from user.domain.user_repository import UserRepository
from user.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from user.security import create_access_token


@pytest.fixture
def client(
        db_session: Session,
) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(settings.DATABASE_URL)
    if not database_exists(engine.url):
        create_database(engine.url)
    return engine


@pytest.fixture(scope="session")
def migrations(
        engine: Engine,
) -> None:
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    alembic_ini = os.path.join(root_dir, "alembic.ini")
    config = Config(alembic_ini)
    upgrade(config, "head")
    yield
    downgrade(config, "base")


@pytest.fixture
def db_session(
        engine: Engine,
        migrations: None,
) -> Generator[Session, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def user_repository() -> UserRepository:
    return SQLAlchemyUserRepository()


@pytest.fixture
def user_admin(
        db_session: Session,
        user_repository: UserRepository,
) -> User:
    return user_repository.get_by_id(db_session, user_id=UUID("6fc330b1-3d65-402c-b7a3-b5b526240505"))


@pytest.fixture
def user_1(
        db_session: Session,
        user_repository: UserRepository,
) -> User:
    user_1 = UserCreate(
        username="user_1",
        password="password",
        is_admin=False,
    )
    return user_repository.create(db_session, user=user_1)


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
