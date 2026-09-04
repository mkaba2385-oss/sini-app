from abc import ABC, abstractmethod
from datetime import date
from typing import Generic, TypeVar

from sini.schemas.parcelle import CultureType
from sini.schemas.prix import PrixResponse
from sini.schemas.user import UserResponse

T = TypeVar("T")


class RepositoryInterface(ABC, Generic[T]):
    @abstractmethod
    def create(self, entity: T) -> T:
        """Crée une entité en laissant le repository générer son identifiant."""
        pass

    @abstractmethod
    def add(self, entity: T) -> T:
        """Ajoute ou met à jour une entité existante."""
        pass

    @abstractmethod
    def get_next_id(self) -> int:
        """Retourne le prochain identifiant (compatibilité InMemory)."""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: int) -> T | None:
        """Récupère une entité par son ID."""
        pass

    @abstractmethod
    def get_all(self) -> list[T]:
        """Retourne toutes les entités."""
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> None:
        """Supprime une entité par son ID."""
        pass


class UserRepositoryInterface(RepositoryInterface[UserResponse]):
    @abstractmethod
    def get_by_phone(self, phone_number: str) -> UserResponse | None:
        """Recherche un utilisateur par son numéro de téléphone."""
        pass


class PrixRepositoryInterface(RepositoryInterface[PrixResponse]):
    """Interface spécialisée pour les relevés de prix."""

    @abstractmethod
    def list_by_culture(
        self,
        culture: CultureType,
    ) -> list[PrixResponse]:
        """Retourne les relevés pour une culture."""
        pass

    @abstractmethod
    def list_by_marche(
        self,
        marche: str,
    ) -> list[PrixResponse]:
        """Retourne les relevés pour un marché."""
        pass

    @abstractmethod
    def delete_by_source_and_date(
        self,
        source: str,
        date_releve: date,
    ) -> None:
        """Supprime les relevés provenant d'une source à une date donnée."""
        pass