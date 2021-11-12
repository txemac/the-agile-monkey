from datetime import datetime
from datetime import timedelta

from jose import jwt
from passlib.context import CryptContext

from src import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
        username: str,
) -> str:
    """
    Create a new access token.

    :param username: username
    :return: access token
    """
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = dict(exp=expire, sub=username)
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    """
    Check the password.

    :param plain_password: plain password
    :param hashed_password: hashed password
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(
        password: str
) -> str:
    """
    Generate a hashed password.

    :param password: password
    :return: hashed password
    """
    return pwd_context.hash(password)
