from datetime import datetime, timezone

from sini.repositories.base import RepositoryInterface
from sini.schemas.diagnostic import (
    DiagnosticCreate,
    DiagnosticResponse,
    DiagnosticUpdate,
)
from sini.schemas.parcelle import ParcelleResponse
from sini.services.exceptions import (
    EntityNotFoundError,
    UnauthorizedAccessError,
)


class DiagnosticService:
    """Service métier de gestion des diagnostics."""

    def __init__(
        self,
        repository: RepositoryInterface[DiagnosticResponse],
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

    def create(
        self,
        data: DiagnosticCreate,
        user_id: int,
    ) -> DiagnosticResponse:
        """Crée un nouveau diagnostic."""

        self._check_parcelle_owner(
            data.parcelle_id,
            user_id,
        )

        diagnostic = DiagnosticResponse(
            id=0,
            created_at=datetime.now(timezone.utc),
            updated_at=None,
            **data.model_dump(),
        )

        return self.repo.create(diagnostic)

    def get_by_id(
        self,
        diagnostic_id: int,
        user_id: int,
    ) -> DiagnosticResponse:
        """Récupère un diagnostic par son ID."""

        diagnostic = self.repo.get_by_id(diagnostic_id)

        if diagnostic is None:
            raise EntityNotFoundError("Diagnostic", diagnostic_id)

        self._check_parcelle_owner(
            diagnostic.parcelle_id,
            user_id,
        )

        return diagnostic

    def get_all(
        self,
        user_id: int,
    ) -> list[DiagnosticResponse]:
        """Retourne uniquement les diagnostics des parcelles de l'utilisateur."""

        diagnostics = self.repo.get_all()

        return [
            diagnostic
            for diagnostic in diagnostics
            if (parcelle := self.parcelle_repo.get_by_id(diagnostic.parcelle_id))
            is not None
            and parcelle.owner_id == user_id
        ]

    def update(
        self,
        diagnostic_id: int,
        data: DiagnosticUpdate,
        user_id: int,
    ) -> DiagnosticResponse:
        """Met à jour un diagnostic."""

        current = self.get_by_id(
            diagnostic_id,
            user_id,
        )

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

    def delete(
        self,
        diagnostic_id: int,
        user_id: int,
    ) -> None:
        """Supprime un diagnostic."""

        self.get_by_id(
            diagnostic_id,
            user_id,
        )

        self.repo.delete(diagnostic_id)
