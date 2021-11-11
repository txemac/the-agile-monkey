from user.domain.user_repository import UserRepository
from user.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository


def di_user_repository() -> UserRepository:
    return SQLAlchemyUserRepository()
