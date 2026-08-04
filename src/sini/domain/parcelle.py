from datetime import datetime, timezone
from typing import List, Optional
from sini.domain.user import User
from sini.domain.journal import JournalEntry
from sini.schemas.parcelle import ParcelleCreate, ParcelleResponse, RegionMali


class Parcelle:
    """Modèle domaine représentant une parcelle agricole."""

    def __init__(
        self,
        parcelle_id: int,
        name: str,
        superficie_ha: float,
        culture: str,
        region: RegionMali,
        owner: User,  # Composition : Une Parcelle A UN User (propriétaire)
        created_at: Optional[datetime] = None,
    ) -> None:
        self.id = parcelle_id
        self.name = name
        self._superficie_ha = superficie_ha
        self.culture = culture
        self.region = region
        self.owner = owner
        self.created_at = created_at or datetime.now(timezone.utc)
        self.journal_entries: List[JournalEntry] = []  # Composition : journal_entries

    @property
    def superficie_ha(self) -> float:
        return self._superficie_ha

    @superficie_ha.setter
    def superficie_ha(self, valeur: float) -> None:
        """Validation via Property."""
        if valeur <= 0:
            raise ValueError("La superficie doit être strictement positive.")
        self._superficie_ha = valeur

    # --- Méthodes Métier ---

    def add_journal_entry(self, entry: JournalEntry) -> None:
        """Ajoute une activité au journal de la parcelle."""
        self.journal_entries.append(entry)

    def total_cout_activites(self) -> float:
        """Calcule le coût total cumulé des opérations sur la parcelle."""
        return sum(entry.cout_fcfa for entry in self.journal_entries)

    # --- Conversions Pont avec Pydantic ---

    @classmethod
    def from_schema(cls, parcelle_id: int, dto: ParcelleCreate, owner: User) -> "Parcelle":
        """Instancie un objet POO Parcelle à partir du DTO Pydantic."""
        return cls(
            parcelle_id=parcelle_id,
            name=dto.name,
            superficie_ha=dto.superficie_ha,
            culture=dto.culture,
            region=dto.region,
            owner=owner,
        )

    def to_schema(self) -> ParcelleResponse:
        """Convertit l'objet POO Domaine vers le DTO Pydantic de réponse."""
        return ParcelleResponse(
            id=self.id,
            name=self.name,
            superficie_ha=self.superficie_ha,
            culture=self.culture,
            region=self.region,
            owner_id=self.owner.id,
            created_at=self.created_at,
        )

    def __repr__(self) -> str:
        return f"<Parcelle id={self.id} name='{self.name}' owner='{self.owner.full_name}'>"