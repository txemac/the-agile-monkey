from sqlalchemy.orm import Session

from database import save
from user.domain.user import User
from user.domain.user_repository import UserRepository
from user.infrastructure.models.sqlalchemy_user import SQLAlchemyUser


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
        user_to_save.password = user.password
        user_to_save.dt_created = user.dt_created
        user_to_save.dt_deleted = user.dt_deleted
        user_to_save.is_admin = user.is_admin

        return save(db_session=db_session, obj=user_to_save)
