import pytest
from pydantic import ValidationError

from sini.schemas import CultureType, ParcelleCreate, RegionMali, UserCreate


def test_user_create_phone_validation_success() -> None:
    """Vérifie qu'un numéro malien valide à 8 chiffres est accepté et nettoyé."""
    user = UserCreate(
        full_name="Moussa Diarra",
        phone_number="+223 70 00 00 00",
        region=RegionMali.BAMAKO,
        password="password123",
    )
    assert user.phone_number == "+22370000000"


@pytest.mark.parametrize(
    "invalid_phone",
    [
        "+22312345678",  # Ne commence pas par 2,5,6,7,8,9
        "+33612345678",  # Indicatif non malien
        "+2237000000",  # 7 chiffres (au lieu de 8)
        "+223700000000",  # 9 chiffres
        "0700000000",  # Pas d'indicatif
    ],
)
def test_user_create_phone_validation_failure(invalid_phone: str) -> None:
    """Vérifie que les numéros invalides sont tous rejetés par la regex."""
    with pytest.raises(ValidationError):
        UserCreate(
            full_name="Test User",
            phone_number=invalid_phone,
            region=RegionMali.BAMAKO,
            password="password123",
        )


def test_parcelle_superficie_must_be_positive() -> None:
    """Vérifie que la superficie doit être strictement supérieure à 0 (gt=0)."""
    with pytest.raises(ValidationError):
        ParcelleCreate(
            name="Champ Invalide",
            superficie_ha=0.0,
            culture=CultureType.MAIS,
            region=RegionMali.SEGOU,
            owner_id=1,
        )
