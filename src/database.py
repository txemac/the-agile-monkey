import logging
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

import settings

logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db() -> SessionLocal:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def save(
        db_session: Session,
        obj: Any,
) -> bool:
    """
    Persist an object at database.
    """
    db_session.add(obj)
    try:
        db_session.commit()
        db_session.refresh(obj)
        return True
    except Exception as e:
        logger.exception(str(e))
        db_session.rollback()
        return False


def commit(
        db_session: Session,
) -> bool:
    """
    Commit
    """
    try:
        db_session.commit()
        return True
    except Exception as e:
        logger.exception(str(e))
        db_session.rollback()
        return False
