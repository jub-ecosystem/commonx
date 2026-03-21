import pytest
from commonx.errors import XError,AlreadyExists

def test_already_exists_metadata():
    err = AlreadyExists(metadata={"resource_id": 123,"entity":"user"})
    x = XError.from_code(code=err.code, metadata=err.metadata)
    print(x)

    # assert err.metadata["resource_id"] == 123