from typing import Optional

from pydantic import BaseModel


class AuthToken(BaseModel):
    access_token: str
    token_type: str

    class Config:
        schema_extra = dict(
            example=dict(
                access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                             ".eyJzdWIiOiJ0aGVfYWdpbGVfbW9ua2V5IiwibmFtZSI6ImhvbGEhIGJ1ZW5hIHBydWViYSBlaCEhIDspIn0"
                             ".bG13yy_XigEkjuOPign9ogIbbb9o1gKi5IErcMA__YQ",
                token_type="Bearer"
            )
        )


class AuthTokenPayload(BaseModel):
    sub: Optional[str] = None


class AuthLogin(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = dict(
            example=dict(
                username="username",
                password="top_secret_password",
            )
        )
