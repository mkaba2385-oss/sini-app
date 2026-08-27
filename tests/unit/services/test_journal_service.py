from datetime import datetime, timezone

from sini.repositories.memory import (
    InMemoryJournalRepository,
    InMemoryParcelleRepository,
)
from sini.schemas.journal import ActionType, JournalEntryCreate
from sini.schemas.parcelle import CultureType, ParcelleResponse
from sini.schemas.user import RegionMali
from sini.services.journal_service import JournalService


def test_journal_service_add_list_and_stats() -> None:
    journal_repository = InMemoryJournalRepository()
    parcelle_repository = InMemoryParcelleRepository()

    parcelle_repository.create(
        ParcelleResponse(
            id=0,
            owner_id=1,
            name="Champ test",
            superficie_ha=2.5,
            culture=CultureType.MAIS,
            region=RegionMali.SEGOU,
            commune=None,
            created_at=datetime.now(timezone.utc),
            updated_at=None,
        )
    )

    service = JournalService(
        journal_repository,
        parcelle_repository,
    )

    service.add_entry(
        JournalEntryCreate(
            parcelle_id=1,
            action_type=ActionType.SEMIS,
            title="Semis du maïs",
            cout_fcfa=1000,
        ),
        user_id=1,
    )

    service.add_entry(
        JournalEntryCreate(
            parcelle_id=1,
            action_type=ActionType.IRRIGATION,
            title="Irrigation",
            cout_fcfa=500,
        ),
        user_id=1,
    )

    service.add_entry(
        JournalEntryCreate(
            parcelle_id=1,
            action_type=ActionType.RECOLTE,
            title="Récolte",
            cout_fcfa=300,
        ),
        user_id=1,
    )

    assert len(service.list_by_parcelle(1, user_id=1)) == 3

    assert service.stats(1, user_id=1) == {
        "parcelle_id": 1,
        "nombre_entrees": 3,
        "cout_total_fcfa": 1800,
    }
