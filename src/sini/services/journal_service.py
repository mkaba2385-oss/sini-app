from datetime import datetime, timezone
from typing import Any

from sini.repositories.base import RepositoryInterface
from sini.schemas.journal import (
    JournalEntryCreate,
    JournalEntryResponse,
    JournalEntryUpdate,
)
from sini.schemas.parcelle import ParcelleResponse
from sini.services.exceptions import (
    EntityNotFoundError,
    UnauthorizedAccessError,
)


class JournalService:
    """Service métier de gestion du journal agricole."""

    def __init__(
        self,
        repository: RepositoryInterface[JournalEntryResponse],
        parcelle_repository: RepositoryInterface[ParcelleResponse],
    ) -> None:
        self.repo = repository
        self.parcelle_repo = parcelle_repository

    def _check_parcelle_owner(
        self,
        parcelle_id: int,
        user_id: int,
    ) -> None:
        """Vérifie que la parcelle appartient à l'utilisateur."""

        parcelle = self.parcelle_repo.get_by_id(parcelle_id)

        if parcelle is None:
            raise EntityNotFoundError("Parcelle", parcelle_id)

        if parcelle.owner_id != user_id:
            raise UnauthorizedAccessError()

    def add_entry(
        self,
        data: JournalEntryCreate,
        user_id: int,
    ) -> JournalEntryResponse:
        """Ajoute une entrée au journal."""

        self._check_parcelle_owner(
            data.parcelle_id,
            user_id,
        )

        entry = JournalEntryResponse(
            id=0,
            created_at=datetime.now(timezone.utc),
            **data.model_dump(),
        )

        return self.repo.create(entry)

    def list_by_parcelle(
        self,
        parcelle_id: int,
        user_id: int,
    ) -> list[JournalEntryResponse]:
        """Retourne les entrées associées à une parcelle."""

        self._check_parcelle_owner(
            parcelle_id,
            user_id,
        )

        return [
            entry for entry in self.repo.get_all() if entry.parcelle_id == parcelle_id
        ]

    def update(
        self,
        entry_id: int,
        data: JournalEntryUpdate,
        user_id: int,
    ) -> JournalEntryResponse:
        """Met à jour une entrée existante."""

        current = self.repo.get_by_id(entry_id)

        if current is None:
            raise EntityNotFoundError("Entrée de journal", entry_id)

        self._check_parcelle_owner(
            current.parcelle_id,
            user_id,
        )

        values = data.model_dump(exclude_unset=True)

        updated = current.model_copy(
            update={
                **values,
                "updated_at": datetime.now(timezone.utc),
            }
        )

        return self.repo.add(updated)

    def delete(
        self,
        entry_id: int,
        user_id: int,
    ) -> None:
        """Supprime une entrée du journal."""

        current = self.repo.get_by_id(entry_id)

        if current is None:
            raise EntityNotFoundError("Entrée de journal", entry_id)

        self._check_parcelle_owner(
            current.parcelle_id,
            user_id,
        )

        self.repo.delete(entry_id)

    def stats(
        self,
        parcelle_id: int,
        user_id: int,
    ) -> dict[str, Any]:
        """Calcule des statistiques simples sur le journal d'une parcelle."""

        entries = self.list_by_parcelle(
            parcelle_id,
            user_id,
        )

        total_cost = sum(entry.cout_fcfa for entry in entries)

        return {
            "parcelle_id": parcelle_id,
            "nombre_entrees": len(entries),
            "cout_total_fcfa": total_cost,
        }
