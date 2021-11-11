from http import HTTPStatus

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from user.domain.user_repository import UserRepository


def test_user_create_ok(
        client: TestClient,
        db_session: Session,
        user_repository: UserRepository,
) -> None:
    count_1 = user_repository.count(db_session)
    data = dict(
        username="monkey",
        password="password",
        is_admin=False,
    )
    response = client.post(
        url="/users",
        json=data
    )
    assert response.status_code == HTTPStatus.CREATED
    count_2 = user_repository.count(db_session)
    assert count_1 + 1 == count_2
