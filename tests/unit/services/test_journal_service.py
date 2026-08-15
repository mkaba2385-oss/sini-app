from sini.repositories.memory import InMemoryJournalRepository
from sini.schemas.journal import ActionType, JournalEntryCreate
from sini.services.journal_service import JournalService


def test_journal_service_add_list_and_stats() -> None:
    service = JournalService(InMemoryJournalRepository())
    service.add_entry(
        JournalEntryCreate(
            parcelle_id=1,
            action_type=ActionType.SEMIS,
            title="Semis du maïs",
            cout_fcfa=1000,
        )
    )
    service.add_entry(
        JournalEntryCreate(
            parcelle_id=1,
            action_type=ActionType.IRRIGATION,
            title="Irrigation",
            cout_fcfa=500,
        )
    )
    service.add_entry(
        JournalEntryCreate(
            parcelle_id=2,
            action_type=ActionType.RECOLTE,
            title="Récolte",
            cout_fcfa=300,
        )
    )
    assert len(service.list_by_parcelle(1)) == 2
    assert service.stats(1) == {
        "parcelle_id": 1,
        "nombre_entrees": 2,
        "cout_total_fcfa": 1500,
    }
