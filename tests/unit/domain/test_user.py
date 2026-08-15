import pytest

from sini.domain.user import User
from sini.schemas.parcelle import RegionMali
from sini.schemas.user import UserRole


def test_user_creation_and_properties() -> None:
    user = User(
        user_id=1,
        full_name="Moussa Coulibaly",
        phone_number="+22370000000",
        role=UserRole.FARMER,
        region=RegionMali.SIKASSO,
    )

    assert user.id == 1
    assert user.full_name == "Moussa Coulibaly"
    assert user.phone_number == "+22370000000"
    assert user.role == UserRole.FARMER
    assert user.region == RegionMali.SIKASSO
    assert user.is_active is True


def test_user_phone_number_is_read_only() -> None:
    user = User(1, "Moussa Coulibaly", "+22370000000")

    # Tenter de modifier un attribut sans setter doit lever un AttributeError
    with pytest.raises(AttributeError):
        user.phone_number = "+22380000000"  # type: ignore


def test_user_deactivation() -> None:
    user = User(1, "Moussa Coulibaly", "+22370000000")
    user.deactivate()

    assert user.is_active is False


def test_user_repr():
    user = User(
        user_id=1,
        full_name="Moussa Diallo",
        phone_number="+22370000000",
        role=UserRole.FARMER,
    )
    assert repr(user) == "<User id=1 name='Moussa Diallo' role='FARMER'>"
