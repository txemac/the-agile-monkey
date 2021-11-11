from http import HTTPStatus

from starlette.testclient import TestClient


def test_health(
    client: TestClient,
) -> None:
    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == dict(status="OK")
