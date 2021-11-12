from typing import List
from typing import Optional

from sqlalchemy.orm import Session

from database import save
from user.domain.user import User
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
        user: User,
    ) -> bool:
        user_to_save = SQLAlchemyUser()
        user_to_save.id = user.id
        user_to_save.username = user.username
        user_to_save.password = get_password_hash(user.password)
        user_to_save.dt_created = user.dt_created
        user_to_save.dt_deleted = user.dt_deleted
        user_to_save.is_admin = user.is_admin
        return save(db_session=db_session, obj=user_to_save)

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
    ) -> List[User]:
        query = db_session.query(SQLAlchemyUser)

        if only_users:
            query = query.filter_by(is_admin=False)

        return query.all()
