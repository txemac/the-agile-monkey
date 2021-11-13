import pytest
from sqlalchemy.orm import Session

from customer.domain.customer import Customer
from customer.domain.customer import CustomerCreate
from customer.domain.customer_repository import CustomerRepository
from customer.infrastructure.repositories.sqlalchemy_customer_repository import SQLAlchemyCustomerRepository
from user.domain.user import User


@pytest.fixture
def customer_repository() -> CustomerRepository:
    return SQLAlchemyCustomerRepository()


@pytest.fixture
def customer_1(
        db_session: Session,
        customer_repository: CustomerRepository,
        user_1: User,
) -> Customer:
    customer_1 = CustomerCreate(
        id="The Agile Monkey",
        name="The agile monkey SL",
        surname="surname",
        photo_url="https://assets.website-files.com/5bea194a3705ec25b27ce94e/5bea1afbc107657eff26fb3d_Logo"
                  "%20the%20agile%20monkeys.svg",
    )
    return customer_repository.create(db_session, customer=customer_1, current_user=user_1)
