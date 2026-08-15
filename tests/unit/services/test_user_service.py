from sini.repositories.memory import InMemoryUserRepository
from sini.schemas.user import Language, RegionMali, UserCreate, UserUpdate
from sini.services.exceptions import EntityNotFoundError, SiniServiceError
from sini.services.user_service import UserService


def make_service() -> UserService:
    return UserService(InMemoryUserRepository())


def make_user() -> UserCreate:
    return UserCreate(
        full_name="Moussa Diarra",
        phone_number="70 00 00 00",
        region=RegionMali.BAMAKO,
        password="password123",
    )


def test_user_service_create_and_get_by_phone() -> None:
    service = make_service()
    user = service.create(make_user())
    assert user.phone_number == "+22370000000"
    assert service.get_by_phone("+22370000000") == user


def test_user_service_duplicate_phone() -> None:
    service = make_service()
    service.create(make_user())
    try:
        service.create(make_user())
    except SiniServiceError:
        pass
    else:
        raise AssertionError("Le doublon de téléphone doit être refusé")


def test_user_service_update_and_deactivate() -> None:
    service = make_service()
    user = service.create(make_user())
    updated = service.update(
        user.id,
        UserUpdate(full_name="Awa Traore", language=Language.BAMBARA),
    )
    assert updated.full_name == "Awa Traore"
    assert updated.language == Language.BAMBARA
    assert service.deactivate(user.id).is_active is False


def test_user_service_missing_user() -> None:
    service = make_service()
    try:
        service.get_by_id(999)
    except EntityNotFoundError:
        pass
    else:
        raise AssertionError("Un utilisateur absent doit lever une exception")
