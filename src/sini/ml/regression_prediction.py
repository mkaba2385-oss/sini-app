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

from sini.schemas.prix import PrixResponse


@dataclass(frozen=True)
class PredictionMetrics:
    """Métriques d'évaluation d'un modèle de prédiction."""

    mae: float
    rmse: float


class PriceRegressionModel:
    """Base commune pour les modèles de régression des prix."""

    def __init__(
        self,
        lag_size: int = 3,
    ) -> None:
        if lag_size <= 0:
            raise ValueError("La taille des lags doit être supérieure à 0.")

        self.lag_size = lag_size

    def _build_training_data(
        self,
        prices: Sequence[PrixResponse],
    ) -> tuple[np.ndarray, np.ndarray]:
        """Construit les variables explicatives et les valeurs cibles."""

        if len(prices) <= self.lag_size:
            raise ValueError(
                "Il faut suffisamment de données historiques pour entraîner le modèle."
            )

        sorted_prices = sorted(
            prices,
            key=lambda price: price.date_releve,
        )

        features: list[list[float]] = []
        targets: list[float] = []

        for index in range(self.lag_size, len(sorted_prices)):
            current = sorted_prices[index]

            lags = [
                sorted_prices[index - lag].prix_moyen
                for lag in range(1, self.lag_size + 1)
            ]

            features.append(
                [
                    *lags,
                    float(current.date_releve.month),
                    float(current.date_releve.year),
                ]
            )

            targets.append(current.prix_moyen)

        return np.array(features), np.array(targets)

    def _build_prediction_features(
        self,
        prices: Sequence[PrixResponse],
        target_date: date,
    ) -> np.ndarray:
        """Construit les variables explicatives pour une nouvelle prédiction."""

        if len(prices) < self.lag_size:
            raise ValueError(
                "Il faut suffisamment de données historiques pour prédire."
            )

        sorted_prices = sorted(
            prices,
            key=lambda price: price.date_releve,
        )

        recent_prices = sorted_prices[-self.lag_size :]

        lags = [price.prix_moyen for price in reversed(recent_prices)]

        return np.array(
            [
                [
                    *lags,
                    float(target_date.month),
                    float(target_date.year),
                ]
            ]
        )

    def evaluate(
        self,
        prices: Sequence[PrixResponse],
        test_size: int = 1,
    ) -> PredictionMetrics:
        """Évalue le modèle sur les derniers relevés chronologiques."""

        if test_size <= 0:
            raise ValueError("La taille du test doit être supérieure à 0.")

        sorted_prices = sorted(
            prices,
            key=lambda price: price.date_releve,
        )

        minimum_size = self.lag_size + test_size

        if len(sorted_prices) < minimum_size:
            raise ValueError(
                "Il faut suffisamment de données pour effectuer l'évaluation."
            )

        train_prices = sorted_prices[:-test_size]
        test_prices = sorted_prices[-test_size:]

        self.fit(train_prices)

        predictions = [
            self.predict(train_prices[: len(train_prices)], price.date_releve)
            for price in test_prices
        ]

        actual = [price.prix_moyen for price in test_prices]

        return PredictionMetrics(
            mae=round(mean_absolute_error(actual, predictions), 2),
            rmse=round(root_mean_squared_error(actual, predictions), 2),
        )

    def fit(
        self,
        prices: Sequence[PrixResponse],
    ) -> None:
        """Entraîne le modèle."""

        raise NotImplementedError

    def predict(
        self,
        prices: Sequence[PrixResponse],
        target_date: date,
    ) -> float:
        """Prédit un prix."""

        raise NotImplementedError


class RidgePricePredictionModel(PriceRegressionModel):
    """Modèle de prédiction basé sur Ridge Regression."""

    def __init__(
        self,
        lag_size: int = 3,
        alpha: float = 1.0,
    ) -> None:
        super().__init__(lag_size=lag_size)

        if alpha <= 0:
            raise ValueError("Le paramètre alpha doit être supérieur à 0.")

        self.alpha = alpha
        self.model = Ridge(alpha=alpha)

    def fit(
        self,
        prices: Sequence[PrixResponse],
    ) -> None:
        """Entraîne le modèle Ridge."""

        features, targets = self._build_training_data(prices)

        self.model.fit(features, targets)

    def predict(
        self,
        prices: Sequence[PrixResponse],
        target_date: date,
    ) -> float:
        """Prédit un prix avec Ridge."""

        self.fit(prices)

        features = self._build_prediction_features(
            prices,
            target_date,
        )

        prediction = self.model.predict(features)[0]

        return round(float(prediction), 2)


class RandomForestPricePredictionModel(PriceRegressionModel):
    """Modèle de prédiction basé sur Random Forest."""

    def __init__(
        self,
        lag_size: int = 3,
        n_estimators: int = 100,
        random_state: int = 42,
        min_samples_leaf: int = 1,
    ) -> None:
        super().__init__(lag_size=lag_size)

        if n_estimators <= 0:
            raise ValueError("Le nombre d'arbres doit être supérieur à 0.")

        if min_samples_leaf <= 0:
            raise ValueError(
                "Le nombre minimal d'échantillons par feuille doit être supérieur à 0."
            )

        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            random_state=random_state,
            min_samples_leaf=min_samples_leaf,
        )

    def fit(
        self,
        prices: Sequence[PrixResponse],
    ) -> None:
        """Entraîne le modèle Random Forest."""

        features, targets = self._build_training_data(prices)

        self.model.fit(features, targets)

    def predict(
        self,
        prices: Sequence[PrixResponse],
        target_date: date,
    ) -> float:
        """Prédit un prix avec Random Forest."""

        self.fit(prices)

        features = self._build_prediction_features(
            prices,
            target_date,
        )

        prediction = self.model.predict(features)[0]

        return round(float(prediction), 2)
