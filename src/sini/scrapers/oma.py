import subprocess
from datetime import date

import httpx

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
        """Transforme le texte du bulletin OMA en relevés de prix."""

        start = text.find("Tableau 2 : Prix Détaillants")

        if start == -1:
            return []

        end = text.find("Tableau 3 : Prix grossistes")

        if end == -1:
            return []

        table_text = text[start:end]

        prices: list[PrixCreate] = []

        cultures = [
            CultureType.MIL,
            CultureType.SORGHO,
            CultureType.MAIS,
        ]

        marches_deux_mots = {
            "Kayes",
            "Koulikoro",
            "Sikasso",
            "Ségou",
            "Mopti",
        }

        marches = {
            "Kayes",
            "Koulikoro",
            "Sikasso",
            "Ségou",
            "Mopti",
            "Tombouctou",
            "Gao",
            "Kidal",
            "Bamako",
        }

        for line in table_text.splitlines():
            parts = line.split()

            if len(parts) < 4:
                continue

            if parts[0] not in marches:
                continue

            if parts[0] in marches_deux_mots:
                marche = " ".join(parts[:2])
                valeurs = parts[2:5]
            else:
                marche = parts[0]
                valeurs = parts[1:4]

            for culture, valeur in zip(cultures, valeurs, strict=True):
                if valeur == "-":
                    continue

                prices.append(
                    PrixCreate(
                        culture=culture,
                        marche=marche,
                        prix_moyen=float(valeur),
                        unite=UnitePrix.KG,
                        date_releve=date_releve,
                    )
                )

        return prices

    def scrape(self, url: str) -> str:
        """Télécharge un bulletin et retourne son contenu texte."""

        pdf_content = self.download_pdf(url)

        return self.extract_text(pdf_content)
