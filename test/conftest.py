import os
from typing import Any
from typing import Generator

import pytest
from alembic.command import downgrade
from alembic.command import upgrade
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from starlette.testclient import TestClient

from database import get_db
from main import app

_db_conn = create_engine(os.getenv("DATABASE_URL"))


@pytest.fixture
def client(
    db: Session,
) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='session')
def engine():
    engine = create_engine(os.getenv("DATABASE_URL"))
    if not database_exists(engine.url):
        create_database(engine.url)
    return engine


@pytest.fixture(scope='session')
def migrations(engine):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    alembic_ini = os.path.join(root_dir, 'alembic.ini')
    config = Config(alembic_ini)
    upgrade(config, 'head')
    yield
    downgrade(config, 'base')


@pytest.fixture
def db_session(engine, migrations) -> Generator[Session, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
