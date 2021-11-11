import pytest
from starlette.testclient import TestClient

from main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
