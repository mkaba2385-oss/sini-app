from datetime import datetime, timezone

from sini.repositories.base import RepositoryInterface
from sini.schemas.photo import (
    PhotoCreate,
    PhotoResponse,
    PhotoUpdate,
)
from sini.services.exceptions import EntityNotFoundError


class PhotoService:
    """Service métier de gestion des photos."""

    def __init__(
        self,
        repository: RepositoryInterface[PhotoResponse],
    ) -> None:
        self.repo = repository

    def create(self, data: PhotoCreate) -> PhotoResponse:
        """Ajoute une nouvelle photo."""

        photo = PhotoResponse(
            id=0,
            created_at=datetime.now(timezone.utc),
            **data.model_dump(),
        )

        return self.repo.create(photo)

    def get_by_id(self, photo_id: int) -> PhotoResponse:
        """Récupère une photo par son ID."""

        photo = self.repo.get_by_id(photo_id)

        if photo is None:
            raise EntityNotFoundError("Photo", photo_id)

        return photo

    def get_all(self) -> list[PhotoResponse]:
        """Retourne toutes les photos."""

        return self.repo.get_all()

    def update(
        self,
        photo_id: int,
        data: PhotoUpdate,
    ) -> PhotoResponse:
        """Met à jour une photo."""

        current = self.get_by_id(photo_id)

        values = data.model_dump(exclude_unset=True)

        if not values:
            return current

        updated = current.model_copy(
            update=values,
        )

        return self.repo.add(updated)

    def delete(self, photo_id: int) -> None:
        """Supprime une photo."""

        self.get_by_id(photo_id)
        self.repo.delete(photo_id)
