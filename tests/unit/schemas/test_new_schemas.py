from sini.schemas import Language, PhotoCreate, UserCreate
from sini.schemas.user import RegionMali


def test_language_enum_and_photo_schema() -> None:
    user = UserCreate(
        full_name="Test User",
        phone_number="0022370000000",
        region=RegionMali.BAMAKO,
        password="password123",
        language=Language.BAMBARA,
    )
    photo = PhotoCreate(parcelle_id=1, url="https://example.com/photo.jpg")
    assert user.language == Language.BAMBARA
    assert user.phone_number == "+22370000000"
    assert photo.parcelle_id == 1
