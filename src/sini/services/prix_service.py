from datetime import date, datetime, timezone

from sini.repositories.base import PrixRepositoryInterface
from sini.schemas.parcelle import CultureType
from sini.schemas.prix import (
    PrixCreate,
    PrixResponse,
    PrixUpdate,
)
from sini.services.exceptions import EntityNotFoundError


class PrixService:
    """Service métier de gestion des relevés de prix."""

    def __init__(
        self,
        repository: PrixRepositoryInterface,
    ) -> None:
        self.repo = repository

    def create(self, data: PrixCreate) -> PrixResponse:
        """Crée un nouveau relevé de prix."""

        prix = PrixResponse(
            id=0,
            created_at=datetime.now(timezone.utc),
            updated_at=None,
            **data.model_dump(),
        )

        return self.repo.create(prix)

    def get_by_id(self, prix_id: int) -> PrixResponse:
        """Récupère un relevé de prix par son ID."""

        prix = self.repo.get_by_id(prix_id)

        if prix is None:
            raise EntityNotFoundError("Prix", prix_id)

        return prix

    def get_all(self) -> list[PrixResponse]:
        """Retourne tous les relevés de prix."""

        return self.repo.get_all()

    def list_by_culture(
        self,
        culture: CultureType,
    ) -> list[PrixResponse]:
        """Retourne les relevés de prix pour une culture."""

        return self.repo.list_by_culture(culture)

    def list_by_marche(
        self,
        marche: str,
    ) -> list[PrixResponse]:
        """Retourne les relevés de prix pour un marché."""

        return self.repo.list_by_marche(marche)

    def update(
        self,
        prix_id: int,
        data: PrixUpdate,
    ) -> PrixResponse:
        """Met à jour un relevé de prix."""

        current = self.get_by_id(prix_id)

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

    def delete(self, prix_id: int) -> None:
        """Supprime un relevé de prix."""

        self.get_by_id(prix_id)
        self.repo.delete(prix_id)

    def delete_by_source_and_date(
        self,
        source: str,
        date_releve: date,
    ) -> None:
        """Supprime les relevés d'une source à une date donnée."""

        self.repo.delete_by_source_and_date(
            source=source,
            date_releve=date_releve,
        )