from datetime import date, datetime, timezone

import pytest

from sini.repositories.memory import (
    InMemoryParcelleRepository,
    InMemoryPrixRepository,
)
from sini.schemas.parcelle import CultureType, ParcelleResponse
from sini.schemas.prix import PrixResponse, UnitePrix
from sini.schemas.user import RegionMali


@pytest.fixture
def repo() -> InMemoryParcelleRepository:
    """Fixture qui fournit un repository propre avant chaque test."""
    return InMemoryParcelleRepository()


@pytest.fixture
def sample_parcelle() -> ParcelleResponse:
    """Fixture fournissant une instance de ParcelleResponse."""
    return ParcelleResponse(
        id=1,
        name="Champ Test",
        superficie_ha=3.0,
        culture=CultureType.MAIS,
        region=RegionMali.SEGOU,
        commune="Pelengana",
        owner_id=10,
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )


@pytest.fixture
def prix_repo() -> InMemoryPrixRepository:
    """Fixture qui fournit un repository de prix propre."""
    return InMemoryPrixRepository()


@pytest.fixture
def sample_prices() -> list[PrixResponse]:
    """Fixture fournissant plusieurs relevés de prix."""
    now = datetime.now(timezone.utc)

    return [
        PrixResponse(
            id=1,
            culture=CultureType.MAIS,
            variete="Gambiaka",
            type_prix="detaillant",
            marche="Marché de Ségou",
            prix_moyen=250.0,
            unite=UnitePrix.KG,
            date_releve=date(2026, 1, 1),
            source="OMA",
            created_at=now,
            updated_at=None,
        ),
        PrixResponse(
            id=2,
            culture=CultureType.MAIS,
            variete="Gambiaka",
            type_prix="detaillant",
            marche="Marché de Bamako",
            prix_moyen=300.0,
            unite=UnitePrix.KG,
            date_releve=date(2026, 1, 8),
            source="OMA",
            created_at=now,
            updated_at=None,
        ),
        PrixResponse(
            id=3,
            culture=CultureType.RIZ,
            variete=None,
            type_prix="detaillant",
            marche="Marché de Ségou",
            prix_moyen=400.0,
            unite=UnitePrix.KG,
            date_releve=date(2026, 1, 15),
            source="OMA",
            created_at=now,
            updated_at=None,
        ),
    ]


def test_add_and_get_by_id(
    repo: InMemoryParcelleRepository, sample_parcelle: ParcelleResponse
) -> None:
    repo.add(sample_parcelle)
    retrieved = repo.get_by_id(1)

    assert retrieved is not None
    assert retrieved.id == 1
    assert retrieved.name == "Champ Test"


def test_get_by_id_returns_none_when_not_found(
    repo: InMemoryParcelleRepository,
) -> None:
    assert repo.get_by_id(999) is None


def test_get_next_id_increments_counter(repo: InMemoryParcelleRepository) -> None:
    id1 = repo.get_next_id()
    id2 = repo.get_next_id()

    assert id1 == 1
    assert id2 == 2


def test_get_all(
    repo: InMemoryParcelleRepository, sample_parcelle: ParcelleResponse
) -> None:
    repo.add(sample_parcelle)
    all_items = repo.get_all()

    assert len(all_items) == 1
    assert all_items[0].id == 1


def test_delete(
    repo: InMemoryParcelleRepository, sample_parcelle: ParcelleResponse
) -> None:
    repo.add(sample_parcelle)
    repo.delete(1)

    assert repo.get_by_id(1) is None


def test_clear(
    repo: InMemoryParcelleRepository, sample_parcelle: ParcelleResponse
) -> None:
    repo.add(sample_parcelle)
    repo.get_next_id()
    repo.clear()

    assert len(repo.get_all()) == 0
    assert repo.get_next_id() == 1


def test_list_by_culture(
    prix_repo: InMemoryPrixRepository,
    sample_prices: list[PrixResponse],
) -> None:
    """Retourne uniquement les prix de la culture demandée."""

    for price in sample_prices:
        prix_repo.add(price)

    results = prix_repo.list_by_culture(CultureType.MAIS)

    assert len(results) == 2
    assert all(price.culture == CultureType.MAIS for price in results)


def test_list_by_marche(
    prix_repo: InMemoryPrixRepository,
    sample_prices: list[PrixResponse],
) -> None:
    """Retourne uniquement les prix du marché demandé."""

    for price in sample_prices:
        prix_repo.add(price)

    results = prix_repo.list_by_marche("Marché de Ségou")

    assert len(results) == 2
    assert all(price.marche == "Marché de Ségou" for price in results)


def test_list_by_culture_and_marche(
    prix_repo: InMemoryPrixRepository,
    sample_prices: list[PrixResponse],
) -> None:
    """Retourne uniquement la série culture + marché + unité demandée."""

    for price in sample_prices:
        prix_repo.add(price)

    results = prix_repo.list_by_culture_and_marche(
        CultureType.MAIS,
        "Marché de Ségou",
        UnitePrix.KG,
    )

    assert len(results) == 1
    assert results[0].id == 1


def test_delete_by_source_and_date(
    prix_repo: InMemoryPrixRepository,
    sample_prices: list[PrixResponse],
) -> None:
    """Supprime uniquement les relevés correspondant à la source et la date."""

    for price in sample_prices:
        prix_repo.add(price)

    prix_repo.delete_by_source_and_date(
        source="OMA",
        date_releve=date(2026, 1, 8),
    )

    assert prix_repo.get_by_id(2) is None
    assert prix_repo.get_by_id(1) is not None
    assert prix_repo.get_by_id(3) is not None
