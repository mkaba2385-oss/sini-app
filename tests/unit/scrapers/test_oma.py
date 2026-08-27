from datetime import date
from unittest.mock import Mock, patch

import httpx
import pytest

from sini.schemas.parcelle import CultureType
from sini.scrapers.oma import OmaScraper


def test_download_pdf_returns_content() -> None:
    scraper = OmaScraper()

    fake_response = Mock()
    fake_response.content = b"fake pdf content"

    with patch(
        "sini.scrapers.oma.httpx.get",
        return_value=fake_response,
    ):
        content = scraper.download_pdf(
            "https://example.com/bulletin.pdf",
        )

    assert content == b"fake pdf content"

    fake_response.raise_for_status.assert_called_once()


def test_download_pdf_raises_http_error() -> None:
    scraper = OmaScraper()

    fake_response = Mock()

    fake_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "HTTP error",
        request=Mock(),
        response=Mock(),
    )

    with (
        patch(
            "sini.scrapers.oma.httpx.get",
            return_value=fake_response,
        ),
        pytest.raises(httpx.HTTPStatusError),
    ):
        scraper.download_pdf(
            "https://example.com/bulletin.pdf",
        )


def test_extract_text_returns_pdf_text() -> None:
    scraper = OmaScraper()

    fake_page_1 = Mock()
    fake_page_1.extract_text.return_value = "Première page"

    fake_page_2 = Mock()
    fake_page_2.extract_text.return_value = "Deuxième page"

    fake_reader = Mock()
    fake_reader.pages = [
        fake_page_1,
        fake_page_2,
    ]

    with patch(
        "sini.scrapers.oma.PdfReader",
        return_value=fake_reader,
    ):
        text = scraper.extract_text(
            b"fake pdf content",
        )

    assert text == "Première page\nDeuxième page"


def test_extract_text_handles_empty_page() -> None:
    scraper = OmaScraper()

    fake_page = Mock()
    fake_page.extract_text.return_value = None

    fake_reader = Mock()
    fake_reader.pages = [fake_page]

    with patch(
        "sini.scrapers.oma.PdfReader",
        return_value=fake_reader,
    ):
        text = scraper.extract_text(
            b"fake pdf content",
        )

    assert text == ""


def test_scrape_downloads_and_extracts_text() -> None:
    scraper = OmaScraper()

    with (
        patch.object(
            scraper,
            "download_pdf",
            return_value=b"fake pdf content",
        ) as mock_download,
        patch.object(
            scraper,
            "extract_text",
            return_value="Contenu du bulletin",
        ) as mock_extract,
    ):
        text = scraper.scrape(
            "https://example.com/bulletin.pdf",
        )

    assert text == "Contenu du bulletin"

    mock_download.assert_called_once_with(
        "https://example.com/bulletin.pdf",
    )

    mock_extract.assert_called_once_with(
        b"fake pdf content",
    )


def test_parse_prices_extracts_prices() -> None:
    text = """
Tableau 2 : Prix Détaillants (FCFA/Kg)

Kayes Centre 300 300 250 350
Tombouctou 240 300 250 -
Gao 275 300 250 300
Bamako 250 300 225 300

Tableau 3 : Prix grossistes (100 Kg en F CFA)
"""

    scraper = OmaScraper()

    prices = scraper.parse_prices(
        text,
        date(2021, 11, 10),
    )

    assert len(prices) == 12


def test_parse_prices_handles_one_word_market() -> None:
    text = """
Tableau 2 : Prix Détaillants (FCFA/Kg)

Tombouctou 240 300 250 -

Tableau 3 : Prix grossistes (100 Kg en F CFA)
"""

    scraper = OmaScraper()

    prices = scraper.parse_prices(
        text,
        date(2021, 11, 10),
    )

    assert len(prices) == 3

    assert prices[0].marche == "Tombouctou"
    assert prices[0].culture == CultureType.MIL
    assert prices[0].prix_moyen == 240.0

    assert prices[1].culture == CultureType.SORGHO
    assert prices[1].prix_moyen == 300.0

    assert prices[2].culture == CultureType.MAIS
    assert prices[2].prix_moyen == 250.0


def test_parse_prices_handles_two_word_market() -> None:
    text = """
Tableau 2 : Prix Détaillants (FCFA/Kg)

Kayes Centre 300 300 250 350

Tableau 3 : Prix grossistes (100 Kg en F CFA)
"""

    scraper = OmaScraper()

    prices = scraper.parse_prices(
        text,
        date(2021, 11, 10),
    )

    assert len(prices) == 3

    assert prices[0].marche == "Kayes Centre"
    assert prices[0].prix_moyen == 300.0

    assert prices[1].marche == "Kayes Centre"
    assert prices[1].prix_moyen == 300.0

    assert prices[2].marche == "Kayes Centre"
    assert prices[2].prix_moyen == 250.0


def test_parse_prices_returns_empty_list_when_table_is_missing() -> None:
    scraper = OmaScraper()

    prices = scraper.parse_prices(
        "Un texte sans tableau de prix.",
        date(2021, 11, 10),
    )

    assert prices == []


def test_parse_prices_returns_empty_list_when_end_table_is_missing() -> None:
    scraper = OmaScraper()

    text = """
    Tableau 2 : Prix Détaillants

    Kayes Centre 300 300 250 350 300
    """

    prices = scraper.parse_prices(
        text,
        date(2021, 11, 10),
    )

    assert prices == []
