from datetime import datetime

from sqlalchemy.orm import Session

from customer.domain.customer import Customer
from customer.domain.customer import CustomerUpdate
from customer.domain.customer_repository import CustomerRepository
from utils import assert_dicts
from utils import assert_lists


def test_count_empty(
        db_session: Session,
        customer_repository: CustomerRepository,
) -> None:
    assert customer_repository.count(db_session) == 0


def test_count_ok(
        db_session: Session,
        customer_repository: CustomerRepository,
        customer_1: Customer,
) -> None:
    assert customer_repository.count(db_session) == 1


def test_create_ok(
        db_session: Session,
        customer_repository: CustomerRepository,
) -> None:
    new_customer = Customer(
        id="The Agile Monkey",
        name="The agile monkey SL",
        surname="surname",
        photo_url="https://assets.website-files.com/5bea194a3705ec25b27ce94e/5bea1afbc107657eff26fb3d_Logo"
                  "%20the%20agile%20monkeys.svg",
        dt_created=datetime.utcnow(),
    )
    count_1 = customer_repository.count(db_session)
    created = customer_repository.create(db_session, customer=new_customer)
    count_2 = customer_repository.count(db_session)

    assert created is True
    assert count_1 + 1 == count_2


def test_update_no_changes(
        db_session: Session,
        customer_repository: CustomerRepository,
        customer_1: Customer,
) -> None:
    new_info = CustomerUpdate()
    customer_repository.update(db_session, customer_id=customer_1.id, new_info=new_info)

    customer_db = customer_repository.get_by_id(db_session, customer_id=customer_1.id)
    assert_dicts(original=customer_db.__dict__, expected=customer_1.__dict__)


def test_update_ok(
        db_session: Session,
        customer_repository: CustomerRepository,
        customer_1: Customer,
) -> None:
    new_info = CustomerUpdate(
        id="new_id",
        name="new_name",
        surname="new_surname",
        photo_url="new_photo_url",
        dt_deleted=datetime.utcnow(),
    )
    customer_repository.update(db_session, customer_id=customer_1.id, new_info=new_info)

    customer_db = customer_repository.get_by_id(db_session, customer_id=new_info.id)
    assert_dicts(original=customer_db.__dict__, expected=new_info.dict())


def test_get_by_id_not_exists(
        db_session: Session,
        customer_repository: CustomerRepository,
) -> None:
    assert customer_repository.get_by_id(db_session=db_session, customer_id="not_exists") is None


def test_get_by_id_ok(
        db_session: Session,
        customer_repository: CustomerRepository,
        customer_1: Customer,
) -> None:
    result = customer_repository.get_by_id(db_session=db_session, customer_id=customer_1.id)
    assert_dicts(original=result.__dict__, expected=customer_1.dict())


def test_get_list_empty(
        db_session: Session,
        customer_repository: CustomerRepository,
) -> None:
    assert customer_repository.get_list(db_session=db_session) == []


def test_get_list_all(
        db_session: Session,
        customer_repository: CustomerRepository,
        customer_1: Customer,
) -> None:
    result = customer_repository.get_list(db_session=db_session)
    original = [customer.__dict__ for customer in result]
    expected = [customer_1.dict()]
    assert_lists(original=original, expected=expected)


def test_get_list_only_actives(
        db_session: Session,
        customer_repository: CustomerRepository,
        customer_1: Customer,
) -> None:
    customer_repository.update(
        db_session=db_session,
        customer_id=customer_1.id,
        new_info=CustomerUpdate(dt_deleted=datetime.utcnow()),
    )
    result = customer_repository.get_list(db_session=db_session, only_actives=True)
    original = [customer.__dict__ for customer in result]
    expected = []
    assert_lists(original=original, expected=expected)
