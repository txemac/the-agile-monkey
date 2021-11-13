from datetime import datetime
from typing import List
from typing import Optional

from sqlalchemy.orm import Session

from customer.domain.customer import Customer
from customer.domain.customer import CustomerCreate
from customer.domain.customer import CustomerUpdate
from customer.domain.customer_repository import CustomerRepository
from customer.infrastructure.models.sqlalchemy_customer import SQLAlchemyCustomer
from database import commit
from database import save
from user.domain.user import User


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
            customer: CustomerCreate,
            current_user: User,
    ) -> Optional[Customer]:
        customer_to_save = SQLAlchemyCustomer()
        customer_to_save.id = customer.id
        customer_to_save.name = customer.name
        customer_to_save.surname = customer.surname
        customer_to_save.photo_url = customer.photo_url
        customer_to_save.dt_created = datetime.utcnow()
        customer_to_save.dt_updated = None
        customer_to_save.dt_deleted = None
        customer_to_save.created_by_id = current_user.id
        customer_to_save.updated_by = None
        created = save(db_session=db_session, obj=customer_to_save)
        return Customer(**customer_to_save.__dict__) if created else None

    @classmethod
    def update(
            cls,
            db_session: Session,
            customer_id: str,
            new_info: CustomerUpdate,
            current_user: User,
    ) -> None:
        customer_db = cls.get_by_id(db_session, customer_id=customer_id)
        for key, value in new_info.dict(exclude_unset=True).items():
            setattr(customer_db, key, value)
        customer_db.updated_by_id = current_user.id
        customer_db.dt_updated = datetime.utcnow()
        commit(db_session=db_session)

    @classmethod
    def get_by_id(
            cls,
            db_session: Session,
            customer_id: str,
    ) -> Optional[Customer]:
        return db_session.query(SQLAlchemyCustomer).get(customer_id)

    @classmethod
    def get_list(
            cls,
            db_session: Session,
            only_actives: bool = True,
    ) -> List[Customer]:
        query = db_session.query(SQLAlchemyCustomer)

        if only_actives:
            query = query.filter_by(dt_deleted=None)

        return query.all()
