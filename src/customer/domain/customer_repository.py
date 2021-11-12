from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional

from sqlalchemy.orm import Session

from customer.domain.customer import Customer
from customer.domain.customer import CustomerUpdate


class CustomerRepository(ABC):

    @classmethod
    @abstractmethod
    def count(
            cls,
            db_session: Session,
    ) -> int:
        """
        Count the number of element in the customer table.

        :param db_session: session of the database
        :return: number of customers
        """
        pass

    @classmethod
    @abstractmethod
    def create(
            cls,
            db_session: Session,
            customer: Customer,
    ) -> bool:
        """
        Persist a new Customer.

        :param db_session: session of the database
        :param customer: Customer to persist
        :return: True if the record was created, False otherwise
        """
        pass

    @classmethod
    @abstractmethod
    def update(
            cls,
            db_session: Session,
            customer_id: str,
            new_info: CustomerUpdate,
    ) -> None:
        """
        Persist a new Customer.

        :param db_session: session of the database
        :param customer_id: customer's ID
        :param new_info: new info
        :return: True if the record was created, False otherwise
        """
        pass

    @classmethod
    @abstractmethod
    def get_by_id(
            cls,
            db_session: Session,
            customer_id: str,
    ) -> Optional[Customer]:
        """
        Searches for a persisted customer by ID and returns it if it exists.

        :param db_session: session of the database
        :param customer_id: customer's ID
        :return: customer if found, None otherwise
        """
        pass

    @classmethod
    @abstractmethod
    def get_list(
            cls,
            db_session: Session,
            only_actives: bool = True,
    ) -> List[Customer]:
        """
        Searches for a persisted customers.
        With the filter only_actives you can search only users actives or all.

        :param db_session: session of the database
        :param only_actives: filter
        :return: users
        """
        pass
