from sini.repositories.base import RepositoryInterface
from sini.schemas.parcelle import ParcelleResponse


class InMemoryParcelleRepository(RepositoryInterface[ParcelleResponse]):
    def __init__(self) -> None:
        self._storage: dict[int, ParcelleResponse] = {}
        self._counter: int = 1

    def add(self, parcelle: ParcelleResponse) -> ParcelleResponse:
        self._storage[parcelle.id] = parcelle
        return parcelle

    def get_next_id(self) -> int:
        next_id = self._counter
        self._counter += 1
        return next_id

    def get_by_id(self, entity_id: int) -> ParcelleResponse | None:
        return self._storage.get(entity_id)

    def get_all(self) -> list[ParcelleResponse]:
        return list(self._storage.values())

    def delete(self, entity_id: int) -> None:
        if entity_id in self._storage:
            del self._storage[entity_id]

    def clear(self) -> None:
        self._storage.clear()
        self._counter = 1
