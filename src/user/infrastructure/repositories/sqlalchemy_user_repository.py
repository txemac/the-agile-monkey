from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID
from uuid import uuid4

from sqlalchemy.orm import Session

from database import commit
from database import save
from user.domain.user import User
from user.domain.user import UserCreate
from user.domain.user import UserUpdate
from user.domain.user_repository import UserRepository
from user.infrastructure.models.sqlalchemy_user import SQLAlchemyUser
from user.security import get_password_hash


class SQLAlchemyUserRepository(UserRepository):

    @classmethod
    def count(
            cls,
            db_session: Session,
    ) -> int:
        return db_session.query(SQLAlchemyUser).count()

    @classmethod
    def create(
            cls,
            db_session: Session,
            user: UserCreate,
    ) -> Optional[User]:
        user_to_save = SQLAlchemyUser()
        user_to_save.id = uuid4()
        user_to_save.username = user.username
        user_to_save.password = get_password_hash(user.password)
        user_to_save.dt_created = datetime.utcnow()
        user_to_save.dt_updated = None
        user_to_save.dt_deleted = None
        user_to_save.is_admin = user.is_admin
        created = save(db_session=db_session, obj=user_to_save)
        return User(**user_to_save.__dict__) if created else None

    @classmethod
    def update(
            cls,
            db_session: Session,
            user_id: UUID,
            new_info: UserUpdate,
    ) -> None:
        if new_info.password:
            new_info.password = get_password_hash(new_info.password)
        user_db = cls.get_by_id(db_session, user_id=user_id)
        for key, value in new_info.dict(exclude_unset=True).items():
            setattr(user_db, key, value)
        user_db.dt_updated = datetime.utcnow()
        commit(db_session=db_session)

    @classmethod
    def get_by_id(
            cls,
            db_session: Session,
            user_id: UUID,
    ) -> Optional[User]:
        return db_session.query(SQLAlchemyUser).get(user_id)

    @classmethod
    def get_by_username(
            cls,
            db_session: Session,
            username: str,
    ) -> Optional[User]:
        return db_session.query(SQLAlchemyUser).filter_by(username=username).first()

    @classmethod
    def get_list(
            cls,
            db_session: Session,
            only_users: bool = True,
            only_actives: bool = True,
    ) -> List[User]:
        query = db_session.query(SQLAlchemyUser)

        if only_users:
            query = query.filter_by(is_admin=False)

        if only_actives:
            query = query.filter_by(dt_deleted=None)

        return query.all()
