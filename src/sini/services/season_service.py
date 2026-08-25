from sini.repositories.base import RepositoryInterface
from sini.schemas.season import (
    SeasonCreate,
    SeasonResponse,
    SeasonUpdate,
)
from sini.services.exceptions import EntityNotFoundError


class SeasonService:
    """Service métier de gestion des saisons."""

    def __init__(
        self,
        repository: RepositoryInterface[SeasonResponse],
    ) -> None:
        self.repo = repository

    def create(self, data: SeasonCreate) -> SeasonResponse:
        """Crée une nouvelle saison."""

        season = SeasonResponse(
            id=0,
            **data.model_dump(),
        )

        return self.repo.create(season)

    def get_by_id(self, season_id: int) -> SeasonResponse:
        """Récupère une saison par son ID."""

        season = self.repo.get_by_id(season_id)

        if season is None:
            raise EntityNotFoundError("Saison", season_id)

        return season

    def get_all(self) -> list[SeasonResponse]:
        """Retourne toutes les saisons."""

        return self.repo.get_all()

    def update(
        self,
        season_id: int,
        data: SeasonUpdate,
    ) -> SeasonResponse:
        """Met à jour une saison."""

        current = self.get_by_id(season_id)

        values = data.model_dump(exclude_unset=True)

        if not values:
            return current

        updated = current.model_copy(
            update=values,
        )

        return self.repo.add(updated)

    def delete(self, season_id: int) -> None:
        """Supprime une saison."""

        self.get_by_id(season_id)
        self.repo.delete(season_id)
