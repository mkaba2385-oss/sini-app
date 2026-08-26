from datetime import datetime, timezone

from sini.repositories.base import RepositoryInterface
from sini.schemas.parcelle import ParcelleResponse
from sini.schemas.photo import (
    PhotoCreate,
    PhotoResponse,
    PhotoUpdate,
)
from sini.services.exceptions import (
    EntityNotFoundError,
    UnauthorizedAccessError,
)


class PhotoService:
    """Service métier de gestion des photos."""

    def __init__(
        self,
        repository: RepositoryInterface[PhotoResponse],
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
        data: PhotoCreate,
        user_id: int,
    ) -> PhotoResponse:
        """Ajoute une nouvelle photo."""

        self._check_parcelle_owner(
            data.parcelle_id,
            user_id,
        )

        photo = PhotoResponse(
            id=0,
            created_at=datetime.now(timezone.utc),
            **data.model_dump(),
        )

        return self.repo.create(photo)

    def get_by_id(
        self,
        photo_id: int,
        user_id: int,
    ) -> PhotoResponse:
        """Récupère une photo par son ID."""

        photo = self.repo.get_by_id(photo_id)

        if photo is None:
            raise EntityNotFoundError("Photo", photo_id)

        self._check_parcelle_owner(
            photo.parcelle_id,
            user_id,
        )

        return photo

    def get_all(
        self,
        user_id: int,
    ) -> list[PhotoResponse]:
        """Retourne uniquement les photos des parcelles de l'utilisateur."""

        photos = self.repo.get_all()

        return [
            photo
            for photo in photos
            if (parcelle := self.parcelle_repo.get_by_id(photo.parcelle_id)) is not None
            and parcelle.owner_id == user_id
        ]

    def update(
        self,
        photo_id: int,
        data: PhotoUpdate,
        user_id: int,
    ) -> PhotoResponse:
        """Met à jour une photo."""

        current = self.get_by_id(
            photo_id,
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
        photo_id: int,
        user_id: int,
    ) -> None:
        """Supprime une photo."""

        self.get_by_id(
            photo_id,
            user_id,
        )

        self.repo.delete(photo_id)
