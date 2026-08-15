import pytest

from sini.domain.journal import JournalEntry
from sini.domain.parcelle import Parcelle
from sini.domain.user import User
from sini.schemas.parcelle import ParcelleCreate, RegionMali
from sini.schemas.user import UserRole


@pytest.fixture
def sample_user() -> User:
    return User(
        user_id=1,
        full_name="Moussa Coulibaly",
        phone_number="+22370000000",
        role=UserRole.FARMER,
        region=RegionMali.SIKASSO,
    )


def test_parcelle_superficie_validation(sample_user: User) -> None:
    parcelle = Parcelle(
        1, "Champ Nord", 3.0, "Maïs", RegionMali.SIKASSO, owner=sample_user
    )

    # Tenter de passer une superficie <= 0 doit lever une erreur
    with pytest.raises(
        ValueError,
        match=(
            "La superficie doit être strictly positive."
            "|strictly positive|strictement positive"
        ),
    ):
        parcelle.superficie_ha = 0.0


def test_parcelle_journal_entries_and_total_cost(sample_user: User) -> None:
    parcelle = Parcelle(
        1, "Champ Nord", 3.0, "Maïs", RegionMali.SIKASSO, owner=sample_user
    )

    entry1 = JournalEntry(
        1, parcelle.id, "Labours", "Préparation sol", cout_fcfa=20000.0
    )
    entry2 = JournalEntry(2, parcelle.id, "Semis", "Graines maïs", cout_fcfa=15000.0)

    parcelle.add_journal_entry(entry1)
    parcelle.add_journal_entry(entry2)

    assert len(parcelle.journal_entries) == 2
    assert parcelle.total_cout_activites() == 35000.0


def test_parcelle_from_and_to_schema(sample_user: User) -> None:
    # 1. Schéma Pydantic entrant
    dto = ParcelleCreate(
        name="Champs Riz",
        superficie_ha=2.5,
        culture="Riz",
        region=RegionMali.SEGOU,
        owner_id=sample_user.id,
    )

    # 2. Conversion DTO -> Objet Domaine POO
    parcelle = Parcelle.from_schema(parcelle_id=101, dto=dto, owner=sample_user)
    assert parcelle.id == 101
    assert parcelle.name == "Champs Riz"
    assert parcelle.owner.full_name == "Moussa Coulibaly"

    # 3. Conversion Objet Domaine -> Schéma Pydantic Réponse
    response_dto = parcelle.to_schema()
    assert response_dto.id == 101
    assert response_dto.owner_id == sample_user.id


def test_parcelle_repr_and_invalid_superficie_setter(sample_user):
    """Vérifie la méthode __repr__ et l'exception sur le setter de superficie_ha."""
    parcelle = Parcelle(
        parcelle_id=1,
        name="Champ Test",
        superficie_ha=5.0,
        culture="Maïs",
        region=RegionMali.BAMAKO,
        owner=sample_user,
    )

    # Test __repr__
    assert (
        repr(parcelle)
        == f"<Parcelle id=1 name='Champ Test' owner='{sample_user.full_name}'>"
    )

    # Test du setter (valeur négative ou nulle)
    with pytest.raises(ValueError, match="strictement positive"):
        parcelle.superficie_ha = 0.0
