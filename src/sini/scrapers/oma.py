import subprocess
from datetime import date

import httpx

from sini.parsers.oma import OmaPriceParser
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

        result = subprocess.run(
            ["pdftotext", "-layout", "-", "-"],
            input=pdf_content,
            capture_output=True,
            check=True,
        )

        return result.stdout.decode("utf-8")

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

        return prices

    def scrape(self, url: str) -> str:
        """Télécharge un bulletin et retourne son contenu texte."""

        pdf_content = self.download_pdf(url)

        return self.extract_text(pdf_content)