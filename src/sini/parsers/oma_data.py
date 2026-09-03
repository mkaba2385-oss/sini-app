from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class OmaPriceRecord:
    """Représente un prix extrait d'un bulletin OMA."""

    date_releve: date
    type_prix: str
    culture: str
    variete: str | None
    marche: str
    prix: float
    unite: str
    source: str