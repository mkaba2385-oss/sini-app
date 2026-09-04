from datetime import date

from sini.parsers.oma_data import OmaPriceRecord
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
        "niébé": CultureType.NIEBE,
        "niebe": CultureType.NIEBE,
        "fonio": CultureType.FONIO,
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

    def parse_tableau_1(
        self,
        text: str,
        date_releve: date,
        source: str = "OMA",
    ) -> list["OmaPriceRecord"]:
        """Extrait les prix aux producteurs du Tableau 1 OMA."""

        from sini.parsers.oma_data import OmaPriceRecord

        start = text.find("Tableau 1 : Prix aux Producteurs")
        end = text.find("Tableau 2 : Prix Détaillants")

        if start == -1 or end == -1:
            return []

        table_text = text[start:end]

        localites = [
            "Bankass",
            "Zangasso",
            "Dioïla",
            "Yorosso",
            "Dougouolo",
            "Bla",
            "Loulouni",
            "Dogofri",
            "Shiango",
            "Dioro",
            "Macina",
            "Niono",
        ]

        cultures = [
            "Mil",
            "Sorgho",
            "Maïs",
            "Riz local Gambiaka",
        ]

        records: list[OmaPriceRecord] = []

        for line in table_text.splitlines():
            parts = line.split()

            if not parts:
                continue

            culture = None

            if line.strip().startswith("Riz local Gambiaka"):
                culture = "Riz"
                variete = "Gambiaka"
            elif parts[0] in cultures:
                culture = parts[0]
                variete = None
            else:
                continue

            values_text = line.split()[len(line.split()) - 12 :]

            if len(values_text) != len(localites):
                continue

            for marche, valeur in zip(
                localites,
                values_text,
                strict=True,
            ):
                if valeur == "-":
                    continue

                try:
                    prix = float(valeur.replace(",", "."))
                except ValueError:
                    continue

                records.append(
                    OmaPriceRecord(
                        date_releve=date_releve,
                        type_prix="producteur",
                        culture=culture,
                        variete=variete,
                        marche=marche,
                        prix=prix,
                        unite="kg",
                        source=source,
                    )
                )

        return records    


    def parse_tableau_2(
        self,
        text: str,
        date_releve: date,
        source: str = "OMA",
    ) -> list[OmaPriceRecord]:
        """Extrait les prix détaillants du Tableau 2 OMA."""

        start = text.find("Tableau 2 : Prix Détaillants")
        end = text.find("Tableau 3 : Prix grossistes")

        if start == -1 or end == -1:
            return []

        table_text = text[start:end]

        colonnes = [
            ("Mil", "Entier"),
            ("Mil", "Pilé"),
            ("Sorgho", "Entier"),
            ("Sorgho", "Pilé"),
            ("Maïs", "Entier"),
            ("Maïs", "Pilé"),
            ("Riz", "BBi"),
            ("Riz", "RM40 i"),
            ("Riz", "Gambiaka"),
            ("Riz", "Etuvé Blanc"),
            ("Riz", "Etuvé Rouge"),
            ("Riz", "BG"),
            ("Niébé", None),
            ("Fonio", None),
        ]

        marches = [
            "Kayes Centre",
            "Koulikoro Ba",
            "Sikasso Centre",
            "Ségou Centre",
            "Mopti Digue",
            "Tombouctou",
            "Gao",
            "Kidal",
            "Bamako",
        ]

        records: list[OmaPriceRecord] = []

        for line in table_text.splitlines():
            parts = line.split()

            if not parts:
                continue

            marche = None
            values: list[str] = []

            for candidate in marches:
                candidate_parts = candidate.split()

                if parts[: len(candidate_parts)] == candidate_parts:
                    marche = candidate
                    values = parts[len(candidate_parts) :]
                    break

            if marche is None or len(values) != len(colonnes):
                continue

            for (culture, variete), valeur in zip(
                colonnes,
                values,
                strict=True,
            ):
                if valeur == "-":
                    continue

                try:
                    prix = float(valeur.replace(",", "."))
                except ValueError:
                    continue

                records.append(
                    OmaPriceRecord(
                        date_releve=date_releve,
                        type_prix="detaillant",
                        culture=culture,
                        variete=variete,
                        marche=marche,
                        prix=prix,
                        unite="kg",
                        source=source,
                    )
                )

        return records


    def parse_tableau_3(
        self,
        text: str,
        date_releve: date,
        source: str = "OMA",
    ) -> list[OmaPriceRecord]:
        """Extrait les prix grossistes du Tableau 3 OMA."""

        start = text.find("Tableau 3 : Prix grossistes")
        end = text.find("Tableau 4 :")

        if start == -1 or end == -1:
            return []

        table_text = text[start:end]

        cultures = {
            "Mil": ("Mil", None),
            "Sorgho": ("Sorgho", None),
            "Maïs jaune": ("Maïs", "Jaune"),
            "Riz RM40 importé": ("Riz", "RM40 importé"),
            "Riz Gambiaka": ("Riz", "Gambiaka"),
            "Riz BB importé": ("Riz", "BB importé"),
        }

        records: list[OmaPriceRecord] = []

        for line in table_text.splitlines():
            line = line.strip()

            if not line:
                continue

            matched_culture = None

            for raw_name, value in cultures.items():
                if line.startswith(raw_name):
                    matched_culture = value
                    prix_raw = line[len(raw_name) :].strip()
                    break

            if matched_culture is None:
                continue

            try:
                prix = float(
                    prix_raw.replace(".", "").replace(",", ".")
                )
            except ValueError:
                continue

            culture, variete = matched_culture

            records.append(
                OmaPriceRecord(
                    date_releve=date_releve,
                    type_prix="grossiste",
                    culture=culture,
                    variete=variete,
                    marche="District de Bamako",
                    prix=prix,
                    unite="100kg",
                    source=source,
                )
            )

        return records


    def parse_tableau_4(
        self,
        text: str,
        date_releve: date,
        source: str = "OMA",
    ) -> list[OmaPriceRecord]:
        """Extrait les prix au détail dans la sous-région."""

        start = text.find("Tableau 4 : Prix au détail")
        end = text.find("Tableau 5:")

        if start == -1 or end == -1:
            return []

        table_text = text[start:end]

        marches = [
            "Bamako Niaréla",
            "Ouagadougou Sankaryaré",
            "Abidjan Adjamé",
            "Dakar Thiaroye",
        ]


        records: list[OmaPriceRecord] = []

        lignes = table_text.splitlines()
        index = 0

        while index < len(lignes):
            line = lignes[index].strip()

            if not line:
                index += 1
                continue

            if line.startswith("Mil"):
                culture = "Mil"
                variete = None
                values = line.split()[1:]
            elif line.startswith("Sorgho"):
                culture = "Sorgho"
                variete = None
                values = line.split()[1:]
            elif line.startswith("Maïs"):
                culture = "Maïs"
                variete = None
                values = line.split()[1:]
            elif line.startswith("Riz de Grande"):
                culture = "Riz"
                variete = "Grande Consommation"

                index += 1

                if index >= len(lignes):
                    break

                values = lignes[index].split()
            elif line.startswith("Riz Local"):
                culture = "Riz"
                variete = "Local"
                values = line.split()[2:]
            else:
                index += 1
                continue

            if len(values) != len(marches):
                index += 1
                continue

            for marche, valeur in zip(marches, values, strict=True):
                if valeur == "-":
                    continue

                try:
                    prix = float(valeur.replace(",", "."))
                except ValueError:
                    continue

                records.append(
                    OmaPriceRecord(
                        date_releve=date_releve,
                        type_prix="detaillant",
                        culture=culture,
                        variete=variete,
                        marche=marche,
                        prix=prix,
                        unite="kg",
                        source=source,
                    )
                )

            index += 1

        return records