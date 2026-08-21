from datetime import datetime, timezone
from typing import Any

from sini.repositories.base import RepositoryInterface
from sini.schemas.journal import (
    JournalEntryCreate,
    JournalEntryResponse,
    JournalEntryUpdate,
)
from sini.services.exceptions import EntityNotFoundError


class JournalService:
    """Service métier de gestion du journal agricole."""

    def __init__(self, repository: RepositoryInterface[JournalEntryResponse]) -> None:
        self.repo = repository

    def add_entry(self, data: JournalEntryCreate) -> JournalEntryResponse:
        """Ajoute une entrée au journal."""
        entry = JournalEntryResponse(
            id=0,
            created_at=datetime.now(timezone.utc),
            **data.model_dump(),
        )
        return self.repo.create(entry)

    def list_by_parcelle(self, parcelle_id: int) -> list[JournalEntryResponse]:
        """Retourne les entrées associées à une parcelle."""
        return [
            entry for entry in self.repo.get_all() if entry.parcelle_id == parcelle_id
        ]

    def update(self, entry_id: int, data: JournalEntryUpdate) -> JournalEntryResponse:
        """Met à jour une entrée existante."""
        current = self.repo.get_by_id(entry_id)
        if current is None:
            raise EntityNotFoundError("Entrée de journal", entry_id)
        values = data.model_dump(exclude_unset=True)
        updated = current.model_copy(
            update={**values, "updated_at": datetime.now(timezone.utc)}
        )
        return self.repo.add(updated)

    def stats(self, parcelle_id: int) -> dict[str, Any]:
        """Calcule des statistiques simples sur le journal d'une parcelle."""
        entries = self.list_by_parcelle(parcelle_id)
        total_cost = sum(entry.cout_fcfa for entry in entries)
        return {
            "parcelle_id": parcelle_id,
            "nombre_entrees": len(entries),
            "cout_total_fcfa": total_cost,
        }
