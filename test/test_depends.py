from typing import Any
from uuid import UUID

import pytest
from fastapi import HTTPException

from user.depends import str_to_uuid


def test_str_to_uuid_ok() -> None:
    assert isinstance(str_to_uuid(uuid="f05acf11-ef44-4e9c-95ea-7699f5fe2d34"), UUID)


@pytest.mark.parametrize("uuid", ["not_valid", 123, "f05acf11-ef44-4e9c"])
def test_str_to_uuid_error(
        uuid: Any,
) -> None:
    with pytest.raises(HTTPException):
        str_to_uuid(uuid=uuid)
