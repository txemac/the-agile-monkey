from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import HTTPException

import messages


def str_to_uuid(
        uuid: str,
) -> Optional[UUID]:
    """
    Check is a str is a valid UUID.
    Return UUID or error.

    :param uuid: string
    :return: UUID
    """
    if uuid is None:
        return None
    try:
        result = UUID(str(uuid))
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=messages.UUID_NOT_VALID)
    return result
