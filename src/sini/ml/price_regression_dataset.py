from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from sklearn.preprocessing import OneHotEncoder  # type: ignore[import-untyped]

from sini.schemas.prix import PrixResponse


def build_global_training_data(
    prices: Sequence[PrixResponse],
    lag_size: int = 3,
) -> tuple[np.ndarray, np.ndarray]:
    """Construit un dataset ML global à partir des prix historiques.

    Les lags sont calculés séparément pour chaque couple
    culture + marché.
    """

    if lag_size <= 0:
        raise ValueError("La taille des lags doit être supérieure à 0.")

    kg_prices = [price for price in prices if price.unite.value == "kg"]

    groups: dict[tuple[str, str], list[PrixResponse]] = {}

    for price in kg_prices:
        key = (
            price.culture.value,
            price.marche,
        )
        groups.setdefault(key, []).append(price)

    rows: list[list[object]] = []
    targets: list[float] = []

    for group_prices in groups.values():
        sorted_prices = sorted(
            group_prices,
            key=lambda price: price.date_releve,
        )

        if len(sorted_prices) <= lag_size:
            continue

        for index in range(lag_size, len(sorted_prices)):
            current = sorted_prices[index]

            lags = [
                sorted_prices[index - lag].prix_moyen for lag in range(1, lag_size + 1)
            ]

            rows.append(
                [
                    *lags,
                    current.date_releve.month,
                    current.date_releve.year,
                    current.culture.value,
                    current.marche,
                ]
            )

            targets.append(current.prix_moyen)

    if not rows:
        raise ValueError(
            "Impossible de construire le dataset : pas assez de données historiques."
        )

    numeric_features = np.array(
        [row[: lag_size + 2] for row in rows],
        dtype=float,
    )

    categorical_features = np.array(
        [row[lag_size + 2 :] for row in rows],
        dtype=str,
    )

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False,
    )

    encoded_categories = encoder.fit_transform(
        categorical_features,
    )

    features = np.hstack(
        [
            numeric_features,
            encoded_categories,
        ]
    )

    return features, np.array(targets)
