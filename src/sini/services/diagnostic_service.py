from datetime import datetime, timezone

from sini.repositories.base import RepositoryInterface
from sini.schemas.diagnostic import (
    DiagnosticCreate,
    DiagnosticResponse,
    DiagnosticUpdate,
)
from sini.services.exceptions import EntityNotFoundError


class DiagnosticService:
    """Service métier de gestion des diagnostics."""

    def __init__(
        self,
        repository: RepositoryInterface[DiagnosticResponse],
    ) -> None:
        self.repo = repository

    def create(self, data: DiagnosticCreate) -> DiagnosticResponse:
        """Crée un nouveau diagnostic."""

        diagnostic = DiagnosticResponse(
            id=0,
            created_at=datetime.now(timezone.utc),
            updated_at=None,
            **data.model_dump(),
        )

        return self.repo.create(diagnostic)

    def get_by_id(self, diagnostic_id: int) -> DiagnosticResponse:
        """Récupère un diagnostic par son ID."""

        diagnostic = self.repo.get_by_id(diagnostic_id)

        if diagnostic is None:
            raise EntityNotFoundError("Diagnostic", diagnostic_id)

        return diagnostic

    def get_all(self) -> list[DiagnosticResponse]:
        """Retourne tous les diagnostics."""

        return self.repo.get_all()

    def update(
        self,
        diagnostic_id: int,
        data: DiagnosticUpdate,
    ) -> DiagnosticResponse:
        """Met à jour un diagnostic."""

        current = self.get_by_id(diagnostic_id)

        values = data.model_dump(exclude_unset=True)

        if not values:
            return current

        updated = current.model_copy(
            update={
                **values,
                "updated_at": datetime.now(timezone.utc),
            }
        )

        return self.repo.add(updated)

    def delete(self, diagnostic_id: int) -> None:
        """Supprime un diagnostic."""

        self.get_by_id(diagnostic_id)
        self.repo.delete(diagnostic_id)
