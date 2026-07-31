from datetime import datetime, timezone
from typing import Iterator 
from sini.schemas.parcelle import (
    ParcelleCreate,
    ParcelleResponse,
    ParcelleUpdate,
    CultureType,
    RegionMali,
)

from .exceptions import EntityNotFoundError
from .utils import timer 

class ParcelleService:
    """Service en mémoire pour la gestion du CRUD des parcelles."""
    def __init__(self) -> None :
        # Stockage en mémoire : ID -> ParcelleResponse
        self._storage: dict[int, ParcelleResponse] = {}
        self._counter: int = 1

    @timer
    def create_parcelle(self, data: ParcelleCreate) -> ParcelleResponse:
        """Crée une nouvelle parcelle et lui attribue un ID unique."""
        parcelle_id = self._counter
        now = datetime.now(timezone.utc)

        # Utilisation de l'unpacking Pydantic (data.model_dump())
        parcelle = ParcelleResponse(
            id=parcelle_id,
            created_at=now,
            updated_at=None,
            **data.model_dump(), 
        )
        self.storage[parcelle_id] = parcelle
        self._counter += 1
        return parcelle 

    @timer
    def get_by_id(self, parcelle_id:int) -> ParcelleResponse:
        """Récupère une parcelle par son ID."""
        if parcelle_id not in self._storage:
            raise EntityNotFoundError("Parcelle", parcelle_id)
        return self._storage[parcelle_id]

    @timer
    def get_all(self) -> list[ParcelleResponse]:
        """Retourne la liste de toutes les parcelles."""
        return list(self._storage.values())

    def stream_by_owner(self, owner_id: int) -> Iterator[ParcelleResponse]:
        """Générateur qui produit les parcelles d'un propriétaire une par une."""
        for parcelle in self._storage.values():
            if parcelle.owner_id == owner_id:
                yield parcelle 

    @timer 
    def filter_parcelles(
        self,
        owner_id: int | None = None,
        region: RegionMali | None = None,
        culture: CultureType | None = None,
        ) -> list[ParcelleResponse]:
        """Filtre les parcelles selon plusieurs critères via une list comprehension."""
        return [
            p for p in self._storage.values()
            if (owner_id is None or p.owner_id == owner_id)
            and (region is None or p.region == region)
            and (culture is None or p.culture == culture)
        ]

    @timer
    def updated_parcelle(self, parcelle_id: int, data: ParcelleUpdate) -> ParcelleResponse:
        """Mise à jour partielle d'une parcelle."""
        current = self.get_by_id(parcelle_id)

        #Extraction des champs modifiés (exclude_unset=True)
        updated_data = data.model_dump(exclude_unset=True)
        if not updated_data:
            return current

        # Création d'un nouveau modèle avec les données mises à jour
        updated_dict = current.model_dump()
        updated_dict.update(updated_data)
        updated_dict["updated_at"] = datetime.now(timezone.utc)

        updated_parcelle = ParcelleResponse(**updated_dict)
        self._storage[parcelle_id] = updated_parcelle
        return updated_parcelle


    @timer 
    def delete_parcelle(self, parcelle_id: int) -> None:
        """Supprime une parcelle."""
        if parcelle_id not in self._storage:
            raise EntityNotFoundError("Parcelle", parcelle_id)
        del self._storage[parcelle_id]

    def clear(self) -> None :
        """Réinitialise le stockage."""
        self._storage.clear()
        self._counter = 1

        
        
     





