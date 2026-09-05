from datetime import date
from pathlib import Path

from sini.db.session import SessionLocal
from sini.factories.service_factory import ServiceFactory
from sini.scrapers.oma import OmaScraper

BULLETINS = [
    (
        "data/oma/communique_du_09_au_15_septembre_2021.pdf",
        date(2021, 9, 15),
    ),
    (
        "data/oma/communique_du_16_au_22_septembre_2021.pdf",
        date(2021, 9, 22),
    ),
    (
        "data/oma/communique_du_23_au_29_septembre_2021.pdf",
        date(2021, 9, 29),
    ),
    (
        "data/oma/communique_du_30_septembre_au_06_octobre_2021_002.pdf",
        date(2021, 10, 6),
    ),
    (
        "data/oma/communique_du_04_au_10_novembre_2021.pdf",
        date(2021, 11, 10),
    ),
]


def main() -> None:
    """Importe plusieurs bulletins OMA dans la base."""

    scraper = OmaScraper()

    with SessionLocal() as session:
        prix_service = ServiceFactory.create_prix_service(
            session=session,
        )

        total = 0

        for file_path, date_releve in BULLETINS:
            path = Path(file_path)

            pdf_content = path.read_bytes()

            text = scraper.extract_text(pdf_content)

            prices = scraper.parse_prices(
                text,
                date_releve,
            )

            prix_service.delete_by_source_and_date(
                source="OMA",
                date_releve=date_releve,
            )

            for price in prices:
                prix_service.create(price)

            total += len(prices)

            print(
                f"{path.name} : "
                f"{len(prices)} prix importés "
                f"pour le {date_releve}."
            )

        session.commit()

    print(f"Total : {total} prix importés avec succès.")


if __name__ == "__main__":
    main()