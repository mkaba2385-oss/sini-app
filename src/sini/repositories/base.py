from abc import ABC, abstractmethod
from typing import Generic, TypeVar

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
