from datetime import date

from sini.parsers.oma import OmaPriceParser
from sini.schemas.parcelle import CultureType
from sini.schemas.prix import UnitePrix


def test_parse_returns_prices() -> None:
    parser = OmaPriceParser()

    text = """
    MAÏS | Marché de Bamako | 250 | kg
    RIZ | Marché de Ségou | 500 | sac
    """

    result = parser.parse(
        text=text,
        date_releve=date(2026, 8, 20),
    )

    assert len(result) == 2

    assert result[0].culture == CultureType.MAIS
    assert result[0].marche == "Marché de Bamako"
    assert result[0].prix_moyen == 250.0
    assert result[0].unite == UnitePrix.KG

    assert result[1].culture == CultureType.RIZ
    assert result[1].marche == "Marché de Ségou"
    assert result[1].prix_moyen == 500.0
    assert result[1].unite == UnitePrix.SAC


def test_parse_ignores_invalid_lines() -> None:
    parser = OmaPriceParser()

    text = """
    Ceci est une ligne invalide
    MAÏS | Marché de Bamako | 250 | kg
    RIZ | Marché de Ségou | mauvais_prix | kg
    CULTURE_INCONNUE | Marché | 300 | kg
    """

    result = parser.parse(
        text=text,
        date_releve=date(2026, 8, 20),
    )

    assert len(result) == 1

    assert result[0].culture == CultureType.MAIS


def test_parse_handles_comma_price() -> None:
    parser = OmaPriceParser()

    text = """
    MAÏS | Marché de Bamako | 250,5 | kg
    """

    result = parser.parse(
        text=text,
        date_releve=date(2026, 8, 20),
    )

    assert len(result) == 1
    assert result[0].prix_moyen == 250.5


def test_parse_ignores_unknown_unit() -> None:
    parser = OmaPriceParser()

    text = """
    MAÏS | Marché de Bamako | 250 | caisse
    """

    result = parser.parse(
        text=text,
        date_releve=date(2026, 8, 20),
    )

    assert result == []
