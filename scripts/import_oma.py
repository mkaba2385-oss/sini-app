from datetime import date
from pathlib import Path

from sini.db.session import SessionLocal
from sini.factories.service_factory import ServiceFactory
from sini.scrapers.oma import OmaScraper


def main() -> None:
    """Importe les prix d'un bulletin OMA dans la base."""

    path = Path(
        "data/oma/communique_du_04_au_10_novembre_2021.pdf"
    )

    date_releve = date(2021, 11, 10)

    scraper = OmaScraper()

    pdf_content = path.read_bytes()

    text = scraper.extract_text(pdf_content)

    prices = scraper.parse_prices(
        text,
        date_releve,
    )

    with SessionLocal() as session:
        prix_service = ServiceFactory.create_prix_service(
            session=session,
        )

        prix_service.delete_by_source_and_date(
            source="OMA",
            date_releve=date_releve,
        )

        for price in prices:
            prix_service.create(price)

        session.commit()

    print(f"{len(prices)} prix importés avec succès.")


if __name__ == "__main__":
    main()