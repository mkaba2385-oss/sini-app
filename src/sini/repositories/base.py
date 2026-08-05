from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class RepositoryInterface(ABC, Generic[T]):
    @abstractmethod
    def add(self, entity: T) -> T:
        """Ajoute ou enregistre une entité."""
        pass

    @abstractmethod
    def get_next_id(self) -> int:
        """Génère le prochain identifiant unique."""
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