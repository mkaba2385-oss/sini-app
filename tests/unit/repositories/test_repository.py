from datetime import datetime, timezone

import pytest

from sini.repositories.memory import InMemoryParcelleRepository
from sini.schemas.parcelle import CultureType, ParcelleResponse
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
