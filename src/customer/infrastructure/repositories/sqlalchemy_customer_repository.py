from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from customer.domain.customer import Customer
from customer.domain.customer_repository import CustomerRepository
from customer.infrastructure.models.sqlalchemy_customer import SQLAlchemyCustomer
from database import save


class SQLAlchemyCustomerRepository(CustomerRepository):

    @classmethod
    def count(
            cls,
            db_session: Session,
    ) -> int:
        return db_session.query(SQLAlchemyCustomer).count()

    @classmethod
    def create(
            cls,
            db_session: Session,
            customer: Customer,
    ) -> bool:
        customer_to_save = SQLAlchemyCustomer()
        customer_to_save.id = customer.id
        customer_to_save.name = customer.name
        customer_to_save.surname = customer.surname
        customer_to_save.photo_url = customer.photo_url
        customer_to_save.dt_created = customer.dt_created
        customer_to_save.dt_deleted = customer.dt_deleted
        return save(db_session=db_session, obj=customer_to_save)

    @classmethod
    def get_by_id(
            cls,
            db_session: Session,
            customer_id: UUID,
    ) -> Optional[Customer]:
        return db_session.query(SQLAlchemyCustomer).get(customer_id)
