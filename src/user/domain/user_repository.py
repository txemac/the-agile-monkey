from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional

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

    @classmethod
    @abstractmethod
    def get_by_username(
            cls,
            db_session: Session,
            username: str,
    ) -> Optional[User]:
        """
        Searches for a persisted user by username "unique" and returns it if it exists.

        :param db_session: session of the database
        :param username: username
        :return: user if found, None otherwise
        """
        pass

    @classmethod
    @abstractmethod
    def get_list(
            cls,
            db_session: Session,
            only_users: bool = True,
    ) -> List[User]:
        """
        Searches for a persisted users. Include myself.
        With the filter only_users you can search only users or all (users and admins).

        :param db_session: session of the database
        :param only_users: filter
        :return: users
        """
        pass
