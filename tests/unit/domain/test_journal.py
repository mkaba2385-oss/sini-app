import pytest
from datetime import date
from sini.domain.journal import JournalEntry
from datetime import datetime, timezone


def test_journal_entry_creation_and_summary() -> None:
    entry = JournalEntry(
        entry_id=1,
        parcelle_id=10,
        action="Engrais",
        description="Sachets NPK",
        cout_fcfa=15000.0,
        entry_date=date(2026, 8, 1),
    )

    assert entry.cout_fcfa == 15000.0
    assert entry.summary() == "[01/08/2026] Engrais: Sachets NPK (15000.0 FCFA)"


def test_journal_entry_negative_cost_raises_error() -> None:
    entry = JournalEntry(1, 10, "Achat", "Pesticide", cout_fcfa=5000.0)

    # Passer un coût négatif doit lever un ValueError
    with pytest.raises(ValueError, match="Le coût d'une activité ne peut pas être négatif."):
        entry.cout_fcfa = -1000.0

from datetime import date

def test_journal_entry_repr():
    entry = JournalEntry(
        entry_id=1,
        parcelle_id=10,
        action="Irrigation",
        description="Arrosage du matin",
        cout_fcfa=5000.0,
        entry_date=date(2026, 8, 1),
    )
    assert "Irrigation" in repr(entry)