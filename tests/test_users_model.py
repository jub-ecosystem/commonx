import pytest
from commonx.models.xolo import User


def test_create_user_success():
    """
    Test creating a User model instance successfully.
    """ 

    user = User(
        username="johndoe",
        email="test@test.com",
        first_name="John",
        last_name="Doe",
        hash_password="",
        key="",
        disabled=False
    )
    print(user)
