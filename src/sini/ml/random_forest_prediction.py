from __future__ import annotations

from collections.abc import Sequence
from datetime import date

import numpy as np
from sklearn.ensemble import RandomForestRegressor  # type: ignore[import-untyped]
from sklearn.preprocessing import OneHotEncoder  # type: ignore[import-untyped]

from sini.schemas.parcelle import CultureType
from sini.schemas.prix import PrixResponse


class RandomForestPricePredictionModel:
    """Modèle Random Forest global pour prédire les prix agricoles."""

    def __init__(
        self,
        lag_size: int = 3,
        n_estimators: int = 100,
        max_depth: int | None = None,
        min_samples_leaf: int = 4,
    ) -> None:
        if lag_size <= 0:
            raise ValueError("La taille des lags doit être supérieure à 0.")

        self.lag_size = lag_size

        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_leaf=min_samples_leaf,
            random_state=42,
        )

        self.encoder = OneHotEncoder(
            handle_unknown="ignore",
            sparse_output=False,
        )

        self._is_fitted = False

    def _build_training_data(
        self,
        prices: Sequence[PrixResponse],
    ) -> tuple[np.ndarray, np.ndarray]:
        """Construit le dataset global d'entraînement."""

        filtered_prices = [price for price in prices if price.unite.value == "kg"]

        grouped: dict[tuple[str, str], list[PrixResponse]] = {}

        for price in filtered_prices:
            key = (
                price.culture.value,
                price.marche,
            )
            grouped.setdefault(key, []).append(price)

        numeric_features: list[list[float]] = []
        categorical_features: list[list[str]] = []
        targets: list[float] = []

        for (culture, marche), group_prices in grouped.items():
            group_prices.sort(
                key=lambda price: price.date_releve,
            )

            if len(group_prices) <= self.lag_size:
                continue

            for index in range(
                self.lag_size,
                len(group_prices),
            ):
                history = group_prices[:index]
                target = group_prices[index]

                recent_prices = history[-self.lag_size :]

                numeric_features.append(
                    [
                        *[price.prix_moyen for price in reversed(recent_prices)],
                        float(target.date_releve.month),
                        float(target.date_releve.year),
                    ],
                )

                categorical_features.append(
                    [
                        culture,
                        marche,
                    ],
                )

                targets.append(target.prix_moyen)

        if not numeric_features:
            raise ValueError(
                "Pas assez de données historiques pour entraîner le modèle."
            )

        encoded_categories = self.encoder.fit_transform(
            categorical_features,
        )

        features_array = np.hstack(
            [
                np.asarray(
                    numeric_features,
                    dtype=float,
                ),
                np.asarray(
                    encoded_categories,
                    dtype=float,
                ),
            ],
        )

        return (
            features_array,
            np.asarray(targets, dtype=float),
        )

    def fit(
        self,
        prices: Sequence[PrixResponse],
    ) -> None:
        """Entraîne le modèle global."""

        features, targets = self._build_training_data(
            prices,
        )

        self.model.fit(
            features,
            targets,
        )

        self._is_fitted = True

    def _build_prediction_features(
        self,
        history: Sequence[PrixResponse],
        culture: CultureType,
        marche: str,
        target_date: date,
    ) -> np.ndarray:
        """Construit les variables pour une prédiction."""

        sorted_history = sorted(
            history,
            key=lambda price: price.date_releve,
        )

        recent_prices = sorted_history[-self.lag_size :]

        if len(recent_prices) < self.lag_size:
            raise ValueError("Pas assez d'historique pour effectuer la prédiction.")

        numeric_features = [
            *[price.prix_moyen for price in reversed(recent_prices)],
            float(target_date.month),
            float(target_date.year),
        ]

        encoded_categories = self.encoder.transform(
            [[culture.value, marche]],
        )

        return np.hstack(
            [
                np.asarray(
                    [numeric_features],
                    dtype=float,
                ),
                np.asarray(
                    encoded_categories,
                    dtype=float,
                ),
            ],
        )

    def predict(
        self,
        prices: Sequence[PrixResponse],
        culture: CultureType,
        marche: str,
        target_date: date,
    ) -> float:
        """Prédit le prix pour une culture, un marché et une date."""

        if not self._is_fitted:
            self.fit(prices)

        history = [
            price
            for price in prices
            if price.unite.value == "kg"
            and price.culture == culture
            and price.marche == marche
            and price.date_releve < target_date
        ]

        if len(history) < self.lag_size:
            raise ValueError("Pas assez d'historique pour effectuer la prédiction.")

        prediction_features = self._build_prediction_features(
            history=history,
            culture=culture,
            marche=marche,
            target_date=target_date,
        )

        prediction = self.model.predict(
            prediction_features,
        )

        return round(float(prediction[0]), 2)
