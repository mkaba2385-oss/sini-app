import pytest
from sini.schemas.parcelle import ParcelleCreate, ParcelleResponse
from sini.schemas.user import RegionMali
from sini.services.exceptions import EntityNotFoundError
from sini.services.parcelle_service import ParcelleService
from sini.schemas.parcelle import ParcelleUpdate, RegionMali
from sini.services.exceptions import EntityNotFoundError


@pytest.fixture
def service() -> ParcelleService:
    """Fixture fournissant une instance fraîche du service pour chaque test."""
    return ParcelleService()


def test_create_parcelle_success(service: ParcelleService) -> None:
    """Vérifie la création d'une parcelle avec des données valides."""
    payload = ParcelleCreate(
        name="Champ Nord",
        superficie_ha=2.5,
        culture="Maïs",
        region=RegionMali.SIKASSO,
        owner_id=1,
    )

    parcelle = service.create_parcelle(payload)

    assert isinstance(parcelle, ParcelleResponse)
    assert parcelle.name == "Champ Nord"
    assert parcelle.superficie_ha == 2.5
    assert parcelle.id is not None


def test_get_parcelle_by_id_success(service: ParcelleService) -> None:
    """Vérifie la récupération d'une parcelle existante par son ID."""
    payload = ParcelleCreate(
        name="Champ Sud",
        superficie_ha=1.8,
        culture="Coton",
        region=RegionMali.SIKASSO,
        owner_id=1,
    )
    created = service.create_parcelle(payload)

    # Récupération de la parcelle
    retrieved = service.get_by_id(created.id)

    assert retrieved.id == created.id
    assert retrieved.name == "Champ Sud"


def test_get_parcelle_not_found_raises_exception(service: ParcelleService) -> None:
    """Vérifie qu'une erreur EntityNotFoundError est levée si l'ID n'existe pas."""
    with pytest.raises(EntityNotFoundError):
        service.get_by_id(9999)


def test_list_parcelles(service: ParcelleService) -> None:
    """Vérifie le listage / filtrage des parcelles enregistrées."""
    p1 = ParcelleCreate(
        name="P1",
        superficie_ha=1.0,
        culture="Riz",
        region=RegionMali.SEGOU,
        owner_id=1,
    )
    p2 = ParcelleCreate(
        name="P2",
        superficie_ha=2.0,
        culture="Mil",
        region=RegionMali.MOPTI,
        owner_id=1,
    )

    service.create_parcelle(p1)
    service.create_parcelle(p2)

    # Utilisation de filter_parcelles() au lieu de list_parcelles()
    parcelles = service.filter_parcelles()

    assert len(parcelles) >= 2

def test_update_parcelle_success(service: ParcelleService) -> None:
    payload = ParcelleCreate(
        name="Champ Test",
        superficie_ha=1.0,
        culture="Riz",
        region=RegionMali.SEGOU,
        owner_id=1,
    )
    created = service.create_parcelle(payload)

    # Utilisation de updated_parcelle() au lieu de update_parcelle()
    updated = service.updated_parcelle(
        created.id,
        ParcelleCreate(
            name="Champ Modifié",
            superficie_ha=2.0,
            culture="Riz",
            region=RegionMali.SEGOU,
            owner_id=1,
        ),
    )
    assert updated.name == "Champ Modifié"


def test_delete_parcelle_success(service: ParcelleService) -> None:
    payload = ParcelleCreate(
        name="À Supprimer",
        superficie_ha=1.0,
        culture="Maïs",
        region=RegionMali.SIKASSO,
        owner_id=1,
    )
    created = service.create_parcelle(payload)

    service.delete_parcelle(created.id)

    with pytest.raises(EntityNotFoundError):
        service.get_by_id(created.id)


# --- Tests des cas d'erreur (EntityNotFoundError) ---


def test_update_parcelle_not_found_raises_exception():
    service = ParcelleService()
    update_dto = ParcelleUpdate(name="Nouveau nom")
    with pytest.raises(EntityNotFoundError):
        service.updated_parcelle(999, update_dto)


def test_delete_parcelle_not_found_raises_exception():
    service = ParcelleService()
    with pytest.raises(EntityNotFoundError):
        service.delete_parcelle(999)