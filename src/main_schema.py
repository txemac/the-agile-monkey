from uuid import UUID

from pydantic import BaseModel


class SchemaHealth(BaseModel):
    status: str

    class Config:
        schema_extra = dict(
            example=dict(
                status="OK",
            )
        )


class SchemaID(BaseModel):
    id: UUID

    class Config:
        schema_extra = dict(
            example=dict(
                id="f05acf11-ef44-4e9c-95ea-7699f5fe2d34",
            )
        )
