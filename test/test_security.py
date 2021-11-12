from user.security import create_access_token
from user.security import get_password_hash
from user.security import verify_password


def test_create_access_token() -> None:
    token = create_access_token(username="monkey")
    assert token.startswith("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")


def test_verify_password_ok() -> None:
    plain_password = "test"
    hashed_password = get_password_hash(password=plain_password)
    assert verify_password(plain_password=plain_password, hashed_password=hashed_password) is True


def test_verify_password_error() -> None:
    plain_password = "test"
    hashed_password = get_password_hash(password=plain_password)
    assert verify_password(plain_password=f"no{plain_password}", hashed_password=hashed_password) is False
