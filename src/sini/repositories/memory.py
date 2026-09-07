from datetime import date
from typing import Any, Generic, Protocol, TypeVar, cast

from typing_extensions import Self

from sini.repositories.base import (
    PrixRepositoryInterface,
    RepositoryInterface,
    UserRepositoryInterface,
)
from sini.schemas.journal import JournalEntryResponse
from sini.schemas.parcelle import CultureType, ParcelleResponse
from sini.schemas.prix import PrixResponse, UnitePrix
from sini.schemas.user import UserResponse


class HasId(Protocol):
    """Décrit une entité possédant un identifiant."""

    id: int

    def model_copy(
        self,
        *,
        update: dict[str, Any] | None = None,
    ) -> Self:
        """Retourne une copie du modèle avec des valeurs modifiées."""
        ...


T = TypeVar("T", bound=HasId)


class InMemoryRepository(RepositoryInterface[T], Generic[T]):
    """Implémentation générique du Repository Pattern en mémoire."""

    def __init__(self) -> None:
        self._storage: dict[int, T] = {}
        self._counter = 1

    def create(self, entity: T) -> T:
        """Crée une entité avec un identifiant généré en mémoire."""
        entity_id = self.get_next_id()
        created = entity.model_copy(update={"id": entity_id})
        self._storage[entity_id] = created
        return created

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
        return cast(list[T], list(self._storage.values()))

    def delete(self, entity_id: int) -> None:
        """Supprime une entité si elle existe."""
        self._storage.pop(entity_id, None)

    def clear(self) -> None:
        """Vide le stockage en mémoire."""
        self._storage.clear()
        self._counter = 1


class InMemoryParcelleRepository(InMemoryRepository[ParcelleResponse]):
    """Repository en mémoire dédié aux parcelles."""


class InMemoryUserRepository(
    InMemoryRepository[UserResponse],
    UserRepositoryInterface,
):
    """Repository en mémoire dédié aux utilisateurs."""

    def get_by_phone(self, phone_number: str) -> UserResponse | None:
        """Recherche un utilisateur par son numéro de téléphone."""
        for user in self._storage.values():
            if user.phone_number == phone_number:
                return user
        return None


class InMemoryJournalRepository(InMemoryRepository[JournalEntryResponse]):
    """Repository en mémoire dédié aux entrées du journal."""


class InMemoryPrixRepository(
    InMemoryRepository[PrixResponse],
    PrixRepositoryInterface,
):
    """Repository en mémoire dédié aux relevés de prix."""

    def list_by_culture(
        self,
        culture: CultureType,
    ) -> list[PrixResponse]:
        """Retourne les relevés pour une culture."""

        return [price for price in self._storage.values() if price.culture == culture]

    def list_by_marche(
        self,
        marche: str,
    ) -> list[PrixResponse]:
        """Retourne les relevés pour un marché."""

        return [price for price in self._storage.values() if price.marche == marche]

    def list_by_culture_and_marche(
        self,
        culture: CultureType,
        marche: str,
        unite: UnitePrix,
    ) -> list[PrixResponse]:
        """Retourne les relevés pour une culture, un marché et une unité."""

        return [
            price
            for price in self._storage.values()
            if price.culture == culture
            and price.marche == marche
            and price.unite == unite
        ]

    def delete_by_source_and_date(
        self,
        source: str,
        date_releve: date,
    ) -> None:
        """Supprime les relevés d'une source à une date donnée."""

        ids_to_delete = [
            price.id
            for price in self._storage.values()
            if price.source == source and price.date_releve == date_releve
        ]

        for price_id in ids_to_delete:
            self._storage.pop(price_id, None)
