from sini.repositories.base import RepositoryInterface
from sini.schemas.harvest import (
    HarvestCreate,
    HarvestResponse,
    HarvestUpdate,
)
from sini.schemas.parcelle import ParcelleResponse
from sini.services.exceptions import (
    EntityNotFoundError,
    UnauthorizedAccessError,
)


class HarvestService:
    """Service métier de gestion des récoltes."""

    def __init__(
        self,
        repository: RepositoryInterface[HarvestResponse],
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
        data: HarvestCreate,
        user_id: int,
    ) -> HarvestResponse:
        """Crée une nouvelle récolte."""

        self._check_parcelle_owner(
            data.parcelle_id,
            user_id,
        )

        harvest = HarvestResponse(
            id=0,
            **data.model_dump(),
        )

        return self.repo.create(harvest)

    def get_by_id(
        self,
        harvest_id: int,
        user_id: int,
    ) -> HarvestResponse:
        """Récupère une récolte par son ID."""

        harvest = self.repo.get_by_id(harvest_id)

        if harvest is None:
            raise EntityNotFoundError("Récolte", harvest_id)

        self._check_parcelle_owner(
            harvest.parcelle_id,
            user_id,
        )

        return harvest

    def get_all(
        self,
        user_id: int,
    ) -> list[HarvestResponse]:
        """Retourne uniquement les récoltes de l'utilisateur."""

        harvests: list[HarvestResponse] = []

        for harvest in self.repo.get_all():
            parcelle = self.parcelle_repo.get_by_id(
                harvest.parcelle_id,
            )

            if parcelle is not None and parcelle.owner_id == user_id:
                harvests.append(harvest)

        return harvests

    def update(
        self,
        harvest_id: int,
        data: HarvestUpdate,
        user_id: int,
    ) -> HarvestResponse:
        """Met à jour une récolte."""

        current = self.get_by_id(
            harvest_id,
            user_id,
        )

        values = data.model_dump(exclude_unset=True)

        if not values:
            return current

        updated = current.model_copy(
            update=values,
        )

        return self.repo.add(updated)

    def delete(
        self,
        harvest_id: int,
        user_id: int,
    ) -> None:
        """Supprime une récolte."""

        self.get_by_id(
            harvest_id,
            user_id,
        )

        self.repo.delete(harvest_id)
