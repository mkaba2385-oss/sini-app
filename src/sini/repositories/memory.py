from typing import Generic, Protocol, TypeVar

from sini.repositories.base import RepositoryInterface
from sini.schemas.journal import JournalEntryResponse
from sini.schemas.parcelle import ParcelleResponse
from sini.schemas.user import UserResponse


class HasId(Protocol):
    """Décrit une entité possédant un identifiant."""

    id: int


T = TypeVar("T", bound=HasId)


class InMemoryRepository(RepositoryInterface[T], Generic[T]):
    """Implémentation générique du Repository Pattern en mémoire."""

    def __init__(self) -> None:
        self._storage: dict[int, T] = {}
        self._counter = 1

    def add(self, entity: T) -> T:
        """Ajoute ou remplace une entité."""
        entity_id = entity.id
        self._storage[entity_id] = entity
        return entity

    def get_next_id(self) -> int:
        """Retourne un identifiant croissant."""
        entity_id = self._counter
        self._counter += 1
        return entity_id

    def get_by_id(self, entity_id: int) -> T | None:
        """Recherche une entité par identifiant."""
        return self._storage.get(entity_id)

    def get_all(self) -> list[T]:
        """Retourne toutes les entités."""
        return list(self._storage.values())

    def delete(self, entity_id: int) -> None:
        """Supprime une entité si elle existe."""
        self._storage.pop(entity_id, None)

    def clear(self) -> None:
        """Vide le stockage en mémoire."""
        self._storage.clear()
        self._counter = 1


class InMemoryParcelleRepository(InMemoryRepository[ParcelleResponse]):
    """Repository en mémoire dédié aux parcelles."""


class InMemoryUserRepository(InMemoryRepository[UserResponse]):
    """Repository en mémoire dédié aux utilisateurs."""


class InMemoryJournalRepository(InMemoryRepository[JournalEntryResponse]):
    """Repository en mémoire dédié aux entrées du journal."""
