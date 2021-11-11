from abc import ABC
from abc import abstractmethod

from sqlalchemy.orm import Session

from user.domain.user import User


class UserRepository(ABC):

    @classmethod
    @abstractmethod
    def count(
        cls,
        db_session: Session,
    ) -> int:
        """
        Count the number of element in the user table.

        :param db_session: session of the database
        :return: number of users
        """
        pass

    @classmethod
    @abstractmethod
    def create(
        cls,
        db_session: Session,
        user: User,
    ) -> bool:
        """
        Persist a new User.

        :param db_session: session of the database
        :param user: User to persist
        :return: True if the record was created, False otherwise
        """
        pass
