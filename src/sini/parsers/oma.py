from datetime import date

from sini.schemas.parcelle import CultureType
from sini.schemas.prix import PrixCreate, UnitePrix


class OmaPriceParser:
    """Transforme les données extraites des bulletins OMA en relevés de prix."""

    CULTURE_MAPPING: dict[str, CultureType] = {
        "coton": CultureType.COTON,
        "mais": CultureType.MAIS,
        "maïs": CultureType.MAIS,
        "riz": CultureType.RIZ,
        "mil": CultureType.MIL,
        "sorgho": CultureType.SORGHO,
        "arachide": CultureType.ARACHIDE,
        "arachides": CultureType.ARACHIDE,
        "maraichage": CultureType.MARAICHAGE,
        "maraîchage": CultureType.MARAICHAGE,
    }

    UNITE_MAPPING: dict[str, UnitePrix] = {
        "kg": UnitePrix.KG,
        "kilogramme": UnitePrix.KG,
        "kilogrammes": UnitePrix.KG,
        "sac": UnitePrix.SAC,
        "tonne": UnitePrix.TONNE,
        "panier": UnitePrix.PANIER,
    }

    def parse(
        self,
        text: str,
        date_releve: date,
    ) -> list[PrixCreate]:
        """Transforme le texte brut en relevés de prix.

        Format intermédiaire attendu :

        MAÏS | Marché de Bamako | 250 | kg
        RIZ | Marché de Ségou | 500 | kg
        """

        prices: list[PrixCreate] = []

        for line in text.splitlines():
            line = line.strip()

            if not line:
                continue

            parts = [part.strip() for part in line.split("|")]

            if len(parts) != 4:
                continue

            culture_raw, marche, prix_raw, unite_raw = parts

            culture = self.CULTURE_MAPPING.get(culture_raw.lower())

            unite = self.UNITE_MAPPING.get(unite_raw.lower())

            if culture is None or unite is None:
                continue

            try:
                prix_moyen = float(prix_raw.replace(",", "."))
            except ValueError:
                continue

            price = PrixCreate(
                culture=culture,
                marche=marche,
                prix_moyen=prix_moyen,
                unite=unite,
                date_releve=date_releve,
            )

            prices.append(price)

        return prices
