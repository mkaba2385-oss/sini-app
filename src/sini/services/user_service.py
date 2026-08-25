from datetime import datetime, timezone

from sini.repositories.base import UserRepositoryInterface
from sini.schemas.user import UserCreate, UserResponse, UserUpdate
from sini.services.exceptions import EntityNotFoundError, SiniServiceError


class UserService:
    """Service métier de gestion des utilisateurs."""

    def __init__(self, repository: UserRepositoryInterface) -> None:
        self.repo = repository

    def create(self, data: UserCreate) -> UserResponse:
        """Crée un utilisateur après vérification de l'unicité du téléphone."""
        if self.get_by_phone(data.phone_number) is not None:
            raise SiniServiceError("Ce numéro de téléphone est déjà utilisé.")
        user = UserResponse(
            id=0,
            created_at=datetime.now(timezone.utc),
            **data.model_dump(exclude={"password"}),
        )
        return self.repo.create(user)

    def get_by_phone(self, phone_number: str) -> UserResponse | None:
        """Recherche un utilisateur par son numéro de téléphone."""
        return self.repo.get_by_phone(phone_number)

    def get_by_id(self, user_id: int) -> UserResponse:
        """Récupère un utilisateur par son identifiant."""
        user = self.repo.get_by_id(user_id)
        if user is None:
            raise EntityNotFoundError("Utilisateur", user_id)
        return user

    def update(self, user_id: int, data: UserUpdate) -> UserResponse:
        """Met à jour un utilisateur existant."""
        current = self.get_by_id(user_id)
        values = data.model_dump(exclude_unset=True)
        if "phone_number" in values:
            existing = self.get_by_phone(values["phone_number"])
            if existing is not None and existing.id != user_id:
                raise SiniServiceError("Ce numéro de téléphone est déjà utilisé.")
        updated = current.model_copy(update=values)
        return self.repo.add(updated)

    def deactivate(self, user_id: int) -> UserResponse:
        """Désactive un utilisateur sans supprimer ses données."""
        return self.update(user_id, UserUpdate(is_active=False))
