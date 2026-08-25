from sini.repositories.base import RepositoryInterface
from sini.schemas.harvest import (
    HarvestCreate,
    HarvestResponse,
    HarvestUpdate,
)
from sini.services.exceptions import EntityNotFoundError


class HarvestService:
    """Service métier de gestion des récoltes."""

    def __init__(
        self,
        repository: RepositoryInterface[HarvestResponse],
    ) -> None:
        self.repo = repository

    def create(self, data: HarvestCreate) -> HarvestResponse:
        """Crée une nouvelle récolte."""

        harvest = HarvestResponse(
            id=0,
            **data.model_dump(),
        )

        return self.repo.create(harvest)

    def get_by_id(self, harvest_id: int) -> HarvestResponse:
        """Récupère une récolte par son ID."""

        harvest = self.repo.get_by_id(harvest_id)

        if harvest is None:
            raise EntityNotFoundError("Récolte", harvest_id)

        return harvest

    def get_all(self) -> list[HarvestResponse]:
        """Retourne toutes les récoltes."""

        return self.repo.get_all()

    def update(
        self,
        harvest_id: int,
        data: HarvestUpdate,
    ) -> HarvestResponse:
        """Met à jour une récolte."""

        current = self.get_by_id(harvest_id)

        values = data.model_dump(exclude_unset=True)

        if not values:
            return current

        updated = current.model_copy(
            update=values,
        )

        return self.repo.add(updated)

    def delete(self, harvest_id: int) -> None:
        """Supprime une récolte."""

        self.get_by_id(harvest_id)
        self.repo.delete(harvest_id)
