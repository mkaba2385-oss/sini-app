from datetime import date

import pytest

from sini.ml.regression_prediction import (
    PredictionMetrics,
    RandomForestPricePredictionModel,
    RidgePricePredictionModel,
)
from sini.schemas.parcelle import CultureType
from sini.schemas.prix import PrixResponse, UnitePrix


def make_price(
    price: float,
    day: int,
    culture: CultureType = CultureType.MAIS,
    market: str = "Bamako",
) -> PrixResponse:
    return PrixResponse(
        id=day,
        culture=culture,
        variete=None,
        type_prix="detaillant",
        marche=market,
        prix_moyen=price,
        unite=UnitePrix.KG,
        date_releve=date(2026, 1, day),
        source="TEST",
        created_at=date(2026, 1, day),
        updated_at=date(2026, 1, day),
    )


@pytest.fixture
def prices() -> list[PrixResponse]:
    return [
        make_price(100, 1),
        make_price(110, 2),
        make_price(120, 3),
        make_price(130, 4),
        make_price(140, 5),
        make_price(150, 6),
    ]


def test_ridge_can_fit_and_predict(prices: list[PrixResponse]) -> None:
    model = RidgePricePredictionModel(lag_size=3)

    model.fit(prices[:5])
    prediction = model.predict(prices[:5], date(2026, 1, 6))

    assert isinstance(prediction, float)
    assert prediction > 0


def test_random_forest_can_fit_and_predict(
    prices: list[PrixResponse],
) -> None:
    model = RandomForestPricePredictionModel(
        lag_size=3,
        n_estimators=50,
        random_state=42,
    )

    model.fit(prices[:5])
    prediction = model.predict(prices[:5], date(2026, 1, 6))

    assert isinstance(prediction, float)
    assert prediction > 0


def test_ridge_evaluate_returns_metrics(
    prices: list[PrixResponse],
) -> None:
    model = RidgePricePredictionModel(lag_size=2)

    metrics = model.evaluate(prices, test_size=1)

    assert isinstance(metrics, PredictionMetrics)
    assert metrics.mae >= 0
    assert metrics.rmse >= 0


def test_random_forest_evaluate_returns_metrics(
    prices: list[PrixResponse],
) -> None:
    model = RandomForestPricePredictionModel(
        lag_size=2,
        n_estimators=50,
        random_state=42,
    )

    metrics = model.evaluate(prices, test_size=1)

    assert isinstance(metrics, PredictionMetrics)
    assert metrics.mae >= 0
    assert metrics.rmse >= 0


def test_ridge_rejects_invalid_lag_size() -> None:
    with pytest.raises(
        ValueError,
        match="taille des lags doit être supérieure à 0",
    ):
        RidgePricePredictionModel(lag_size=0)


def test_random_forest_rejects_invalid_lag_size() -> None:
    with pytest.raises(
        ValueError,
        match="taille des lags doit être supérieure à 0",
    ):
        RandomForestPricePredictionModel(lag_size=0)


def test_evaluate_rejects_insufficient_history(
    prices: list[PrixResponse],
) -> None:
    model = RidgePricePredictionModel(lag_size=3)

    with pytest.raises(ValueError):
        model.evaluate(prices[:3], test_size=1)
