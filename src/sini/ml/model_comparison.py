from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

import numpy as np
from sklearn.ensemble import RandomForestRegressor  # type: ignore[import-untyped]
from sklearn.linear_model import Ridge  # type: ignore[import-untyped]
from sklearn.metrics import (  # type: ignore[import-untyped]
    mean_absolute_error,
    root_mean_squared_error,
)
from sklearn.preprocessing import OneHotEncoder  # type: ignore[import-untyped]

from sini.ml.price_prediction import PricePredictionModel
from sini.schemas.prix import PrixResponse


@dataclass(frozen=True)
class ModelComparisonResult:
    """Résultats de comparaison d'un modèle."""

    model_name: str
    mae: float
    rmse: float


def _group_prices(
    prices: Sequence[PrixResponse],
) -> dict[tuple[str, str], list[PrixResponse]]:
    """Regroupe les prix en kg par culture et marché."""

    groups: dict[tuple[str, str], list[PrixResponse]] = {}

    for price in prices:
        if price.unite.value != "kg":
            continue

        key = (
            price.culture.value,
            price.marche,
        )

        groups.setdefault(key, []).append(price)

    for group in groups.values():
        group.sort(key=lambda price: price.date_releve)

    return groups


def _build_features(
    history: Sequence[PrixResponse],
    culture: str,
    marche: str,
    lag_size: int,
) -> list[float]:
    """Construit les variables d'entrée pour une prédiction."""

    sorted_history = sorted(
        history,
        key=lambda price: price.date_releve,
    )

    recent_prices = sorted_history[-lag_size:]

    if len(recent_prices) < lag_size:
        raise ValueError("Pas assez d'historique pour construire les lags.")

    return [
        *[price.prix_moyen for price in reversed(recent_prices)],
        float(sorted_history[-1].date_releve.month),
        float(sorted_history[-1].date_releve.year),
    ]


def _build_global_training_data(
    groups: dict[tuple[str, str], list[PrixResponse]],
    cutoff_date: date,
    lag_size: int,
) -> tuple[np.ndarray, np.ndarray, list[list[str]]]:
    """Construit les données d'entraînement avant la date de test."""

    numeric_features: list[list[float]] = []
    categorical_features: list[list[str]] = []
    targets: list[float] = []

    for (culture, marche), group in groups.items():
        training_prices = [price for price in group if price.date_releve < cutoff_date]

        training_prices.sort(
            key=lambda price: price.date_releve,
        )

        for index in range(lag_size, len(training_prices)):
            history = training_prices[:index]
            target = training_prices[index]

            features = _build_features(
                history,
                culture,
                marche,
                lag_size,
            )

            numeric_features.append(features)
            categorical_features.append([culture, marche])
            targets.append(target.prix_moyen)

    if not numeric_features:
        raise ValueError("Pas assez de données pour entraîner les modèles.")

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False,
    )

    encoded_categories = encoder.fit_transform(
        categorical_features,
    )

    features_array = np.hstack(
        [
            np.asarray(numeric_features, dtype=float),
            np.asarray(encoded_categories, dtype=float),
        ],
    )

    return (
        features_array,
        np.asarray(targets, dtype=float),
        categorical_features,
    )


def _build_test_data(
    test_groups: list[tuple[tuple[str, str], PrixResponse, list[PrixResponse]]],
    encoder: OneHotEncoder,
    lag_size: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Construit les données de test."""

    numeric_features: list[list[float]] = []
    categorical_features: list[list[str]] = []
    targets: list[float] = []

    for (culture, marche), test_price, history in test_groups:
        features = _build_features(
            history,
            culture,
            marche,
            lag_size,
        )

        numeric_features.append(features)
        categorical_features.append([culture, marche])
        targets.append(test_price.prix_moyen)

    encoded_categories = encoder.transform(
        categorical_features,
    )

    features_array = np.hstack(
        [
            np.asarray(numeric_features, dtype=float),
            np.asarray(encoded_categories, dtype=float),
        ],
    )

    return (
        features_array,
        np.asarray(targets, dtype=float),
    )


def compare_regression_models(
    prices: Sequence[PrixResponse],
    lag_size: int = 3,
) -> list[ModelComparisonResult]:
    """
    Compare le modèle actuel, Ridge et Random Forest.

    Les trois modèles sont évalués sur exactement
    les mêmes observations de test.
    """

    groups = _group_prices(prices)

    if not groups:
        raise ValueError("Aucune donnée de prix disponible.")

    # On utilise la dernière date disponible comme date de test.
    latest_date = max(price.date_releve for group in groups.values() for price in group)

    test_groups: list[tuple[tuple[str, str], PrixResponse, list[PrixResponse]]] = []

    for key, group in groups.items():
        history = [price for price in group if price.date_releve < latest_date]

        test_prices = [price for price in group if price.date_releve == latest_date]

        if len(history) >= lag_size and test_prices:
            test_groups.append(
                (
                    key,
                    test_prices[0],
                    history,
                )
            )

    if not test_groups:
        raise ValueError("Pas assez de données pour construire le jeu de test.")

    # Toutes les données avant la date de test servent à l'entraînement.
    x_train, y_train, categories = _build_global_training_data(
        groups,
        latest_date,
        lag_size,
    )

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False,
    )

    encoder.fit(categories)

    x_test, y_test = _build_test_data(
        test_groups,
        encoder,
        lag_size,
    )

    # ---------------------------------------------------------
    # Modèle actuel
    # ---------------------------------------------------------

    baseline_predictions: list[float] = []

    for (_, marche), test_price, history in test_groups:
        model = PricePredictionModel(
            window_size=lag_size,
        )

        prediction = model.predict(
            prices=history,
            culture=test_price.culture,
            marche=marche,
            target_date=test_price.date_releve,
        )

        baseline_predictions.append(prediction)

    # ---------------------------------------------------------
    # Ridge Regression
    # ---------------------------------------------------------

    ridge = Ridge(alpha=1.0)

    ridge.fit(
        x_train,
        y_train,
    )

    ridge_predictions = ridge.predict(x_test)

    # ---------------------------------------------------------
    # Random Forest
    # ---------------------------------------------------------

    forest = RandomForestRegressor(
        n_estimators=100,
        max_depth=None,
        min_samples_leaf=4,
        random_state=42,
    )

    forest.fit(
        x_train,
        y_train,
    )

    forest_predictions = forest.predict(x_test)

    # ---------------------------------------------------------
    # Résultats
    # ---------------------------------------------------------

    return [
        ModelComparisonResult(
            model_name="Modèle actuel",
            mae=round(
                float(
                    mean_absolute_error(
                        y_test,
                        baseline_predictions,
                    )
                ),
                2,
            ),
            rmse=round(
                float(
                    root_mean_squared_error(
                        y_test,
                        baseline_predictions,
                    )
                ),
                2,
            ),
        ),
        ModelComparisonResult(
            model_name="Ridge Regression",
            mae=round(
                float(
                    mean_absolute_error(
                        y_test,
                        ridge_predictions,
                    )
                ),
                2,
            ),
            rmse=round(
                float(
                    root_mean_squared_error(
                        y_test,
                        ridge_predictions,
                    )
                ),
                2,
            ),
        ),
        ModelComparisonResult(
            model_name="Random Forest",
            mae=round(
                float(
                    mean_absolute_error(
                        y_test,
                        forest_predictions,
                    )
                ),
                2,
            ),
            rmse=round(
                float(
                    root_mean_squared_error(
                        y_test,
                        forest_predictions,
                    )
                ),
                2,
            ),
        ),
    ]
