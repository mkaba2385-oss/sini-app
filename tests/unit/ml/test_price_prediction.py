from datetime import date, datetime, timezone

import pytest

from sini.ml.price_prediction import PricePredictionModel
from sini.schemas.parcelle import CultureType
from sini.schemas.prix import PrixResponse, UnitePrix


def create_price(
    price: float,
    recorded_date: date,
) -> PrixResponse:
    """Crée un relevé de prix pour les tests."""

    return PrixResponse(
        id=1,
        culture=CultureType.MAIS,
        variete="Gambiaka",
        type_prix="detaillant",
        marche="Marché de Ségou",
        prix_moyen=price,
        unite=UnitePrix.KG,
        date_releve=recorded_date,
        source="OMA",
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )


def test_predict_uses_moving_average() -> None:
    """La prédiction utilise la moyenne des derniers relevés."""

    model = PricePredictionModel(window_size=3)

    prices = [
        create_price(250.0, date(2026, 1, 1)),
        create_price(270.0, date(2026, 1, 8)),
        create_price(280.0, date(2026, 1, 15)),
    ]

    prediction = model.predict(
        prices,
        date(2026, 2, 1),
    )

    assert prediction == 266.67


def test_predict_uses_only_window_size() -> None:
    """Seuls les derniers relevés de la fenêtre sont utilisés."""

    model = PricePredictionModel(window_size=2)

    prices = [
        create_price(100.0, date(2026, 1, 1)),
        create_price(200.0, date(2026, 1, 8)),
        create_price(300.0, date(2026, 1, 15)),
    ]

    prediction = model.predict(
        prices,
        date(2026, 2, 1),
    )

    assert prediction == 250.0


def test_predict_applies_seasonality() -> None:
    """La prédiction applique un facteur saisonnier."""

    model = PricePredictionModel(window_size=2)

    prices = [
        create_price(100.0, date(2026, 1, 1)),
        create_price(100.0, date(2026, 1, 8)),
        create_price(200.0, date(2026, 2, 1)),
        create_price(200.0, date(2026, 2, 8)),
    ]

    prediction = model.predict(
        prices,
        date(2026, 2, 15),
    )

    assert prediction == 266.67


def test_predict_without_seasonal_history() -> None:
    """Sans historique pour le mois cible, aucun ajustement n'est appliqué."""

    model = PricePredictionModel(window_size=2)

    prices = [
        create_price(100.0, date(2026, 1, 1)),
        create_price(200.0, date(2026, 1, 8)),
    ]

    prediction = model.predict(
        prices,
        date(2026, 3, 1),
    )

    assert prediction == 150.0


def test_predict_without_historical_data() -> None:
    """Une prédiction sans historique doit échouer."""

    model = PricePredictionModel()

    with pytest.raises(
        ValueError,
        match="sans données historiques",
    ):
        model.predict([], date(2026, 2, 1))


def test_model_rejects_invalid_window_size() -> None:
    """Une fenêtre de taille invalide doit échouer."""

    with pytest.raises(
        ValueError,
        match="supérieure à 0",
    ):
        PricePredictionModel(window_size=0)
