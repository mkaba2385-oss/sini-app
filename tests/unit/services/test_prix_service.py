from datetime import date, datetime, timezone

from sini.repositories.memory import InMemoryPrixRepository
from sini.schemas.parcelle import CultureType
from sini.schemas.prix import PrixResponse, UnitePrix
from sini.services.prix_service import PrixService


def create_price(
    price: float,
    recorded_date: date,
    culture: CultureType = CultureType.MAIS,
    marche: str = "Marché de Ségou",
) -> PrixResponse:
    """Crée un relevé de prix pour les tests."""
    return PrixResponse(
        id=0,
        culture=culture,
        variete="Gambiaka",
        type_prix="detaillant",
        marche=marche,
        prix_moyen=price,
        unite=UnitePrix.KG,
        date_releve=recorded_date,
        source="OMA",
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )


def test_list_by_culture_and_marche() -> None:
    repository = InMemoryPrixRepository()

    repository.create(
        create_price(
            250.0,
            date(2026, 1, 1),
            CultureType.MAIS,
            "Marché de Ségou",
        )
    )
    repository.create(
        create_price(
            300.0,
            date(2026, 1, 8),
            CultureType.MAIS,
            "Marché de Bamako",
        )
    )
    repository.create(
        create_price(
            400.0,
            date(2026, 1, 15),
            CultureType.RIZ,
            "Marché de Ségou",
        )
    )

    service = PrixService(repository)

    prices = service.list_by_culture_and_marche(
        culture=CultureType.MAIS,
        marche="Marché de Ségou",
        unite=UnitePrix.KG,
    )

    assert len(prices) == 1
    assert prices[0].prix_moyen == 250.0
    assert prices[0].culture == CultureType.MAIS
    assert prices[0].marche == "Marché de Ségou"


def test_predict_price() -> None:
    repository = InMemoryPrixRepository()

    repository.create(
        create_price(
            100.0,
            date(2026, 1, 1),
            CultureType.MAIS,
            "Marché de Ségou",
        )
    )
    repository.create(
        create_price(
            200.0,
            date(2026, 1, 8),
            CultureType.MAIS,
            "Marché de Ségou",
        )
    )
    repository.create(
        create_price(
            300.0,
            date(2026, 1, 15),
            CultureType.MAIS,
            "Marché de Ségou",
        )
    )

    service = PrixService(repository)

    prediction = service.predict_price(
        culture=CultureType.MAIS,
        marche="Marché de Ségou",
        target_date=date(2026, 2, 1),
    )

    assert prediction == 200.0


def test_predict_price_uses_only_selected_market() -> None:
    repository = InMemoryPrixRepository()

    repository.create(
        create_price(
            100.0,
            date(2026, 1, 1),
            CultureType.MAIS,
            "Marché de Ségou",
        )
    )
    repository.create(
        create_price(
            200.0,
            date(2026, 1, 8),
            CultureType.MAIS,
            "Marché de Ségou",
        )
    )
    repository.create(
        create_price(
            300.0,
            date(2026, 1, 15),
            CultureType.MAIS,
            "Marché de Bamako",
        )
    )

    service = PrixService(repository)

    prediction = service.predict_price(
        culture=CultureType.MAIS,
        marche="Marché de Ségou",
        target_date=date(2026, 2, 1),
    )

    assert prediction == 150.0
