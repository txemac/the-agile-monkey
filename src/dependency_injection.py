from customer.domain.customer_repository import CustomerRepository
from customer.infrastructure.repositories.sqlalchemy_customer_repository import SQLAlchemyCustomerRepository
from user.domain.user_repository import UserRepository
from user.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository


def di_user_repository() -> UserRepository:
    return SQLAlchemyUserRepository()


def di_customer_repository() -> CustomerRepository:
    return SQLAlchemyCustomerRepository()
