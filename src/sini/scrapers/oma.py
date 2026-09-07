from datetime import date
from io import BytesIO

import httpx
from pypdf import PdfReader

from sini.parsers.oma import OmaPriceParser
from sini.schemas.parcelle import CultureType
from sini.schemas.prix import PrixCreate, UnitePrix


class OmaScraper:
    """Scraper permettant de récupérer le contenu des bulletins OMA."""

    def download_pdf(self, url: str) -> bytes:
        """Télécharge un bulletin PDF depuis son URL."""

        response = httpx.get(
            url,
            timeout=30.0,
        )

        response.raise_for_status()

        return response.content

    def extract_text(self, pdf_content: bytes) -> str:
        """Extrait le texte d'un fichier PDF."""

        reader = PdfReader(BytesIO(pdf_content))

        pages_text: list[str] = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages_text.append(text)

        return "\n".join(pages_text)

    def parse_prices(
        self,
        text: str,
        date_releve: date,
    ) -> list[PrixCreate]:
        """Transforme le tableau 2 du bulletin OMA en relevés de prix."""

        parser = OmaPriceParser()

        records = parser.parse_tableau_2(
            text=text,
            date_releve=date_releve,
        )

        prices: list[PrixCreate] = []

        for record in records:
            culture = OmaPriceParser.CULTURE_MAPPING.get(
                record.culture.lower(),
            )

            if culture is None:
                continue

            prices.append(
                PrixCreate(
                    culture=culture,
                    variete=record.variete,
                    type_prix=record.type_prix,
                    marche=record.marche,
                    prix_moyen=record.prix,
                    unite=UnitePrix.KG,
                    date_releve=record.date_releve,
                    source=record.source,
                )
            )

        if prices:
            return prices

        return self._parse_simple_table(text, date_releve)

    def _parse_simple_table(
        self,
        text: str,
        date_releve: date,
    ) -> list[PrixCreate]:
        """Parse le format simplifié utilisé par certains textes OMA."""

        start = text.find("Tableau 2 : Prix Détaillants")
        end = text.find("Tableau 3 : Prix grossistes")

        if start == -1 or end == -1:
            return []

        table_text = text[start:end]

        cultures = [
            CultureType.MIL,
            CultureType.SORGHO,
            CultureType.MAIS,
        ]

        prices: list[PrixCreate] = []

        for line in table_text.splitlines():
            parts = line.split()

            if not parts:
                continue

            if parts[0].lower() == "tableau":
                continue

            if len(parts) < 4:
                continue

            values_start = None

            for index, part in enumerate(parts):
                try:
                    float(part.replace(",", "."))
                    values_start = index
                    break
                except ValueError:
                    continue

            if values_start is None:
                continue

            marche = " ".join(parts[:values_start])
            values = parts[values_start:]

            if not marche or len(values) < 3:
                continue

            for culture, valeur in zip(
                cultures,
                values[:3],
                strict=False,
            ):
                if valeur == "-":
                    continue

                try:
                    prix = float(valeur.replace(",", "."))
                except ValueError:
                    continue

                prices.append(
                    PrixCreate(
                        culture=culture,
                        variete=None,
                        type_prix="detaillant",
                        marche=marche,
                        prix_moyen=prix,
                        unite=UnitePrix.KG,
                        date_releve=date_releve,
                        source="OMA",
                    )
                )

        return prices

    def scrape(self, url: str) -> str:
        """Télécharge un bulletin et retourne son contenu texte."""

        pdf_content = self.download_pdf(url)

        return self.extract_text(pdf_content)
