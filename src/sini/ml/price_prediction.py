from __future__ import annotations

from collections.abc import Sequence
from datetime import date

from sini.schemas.parcelle import CultureType
from sini.schemas.prix import PrixResponse


class PricePredictionModel:
    """Baseline simple de prédiction des prix agricoles.

    La prédiction combine :
    - une moyenne mobile des derniers relevés ;
    - un ajustement saisonnier basé sur le mois.
    """

    def __init__(
        self,
        window_size: int = 3,
    ) -> None:
        if window_size <= 0:
            raise ValueError("La taille de la fenêtre doit être supérieure à 0.")

        self.window_size = window_size

    def predict(
        self,
        prices: Sequence[PrixResponse],
        culture: CultureType,
        marche: str,
        target_date: date,
    ) -> float:
        """Prédit le prix pour une culture, un marché et une date donnée."""

        filtered_prices = [
            price
            for price in prices
            if price.culture == culture
            and price.marche == marche
            and price.date_releve < target_date
        ]

        if not filtered_prices:
            raise ValueError("Impossible de prédire un prix sans données historiques.")

        sorted_prices = sorted(
            filtered_prices,
            key=lambda price: price.date_releve,
        )

        recent_prices = sorted_prices[-self.window_size :]

        moving_average = sum(price.prix_moyen for price in recent_prices) / len(
            recent_prices
        )

        seasonal_factor = self._seasonal_factor(
            sorted_prices,
            target_date,
        )

        prediction = moving_average * seasonal_factor

        return round(prediction, 2)

    def _seasonal_factor(
        self,
        prices: Sequence[PrixResponse],
        target_date: date,
    ) -> float:
        """Calcule un facteur saisonnier simple.

        Le facteur compare le prix moyen du mois cible
        au prix moyen global des données historiques.
        """

        if not prices:
            return 1.0

        global_average = sum(price.prix_moyen for price in prices) / len(prices)

        if global_average <= 0:
            return 1.0

        monthly_prices = [
            price.prix_moyen
            for price in prices
            if price.date_releve.month == target_date.month
        ]

        if not monthly_prices:
            return 1.0

        monthly_average = sum(monthly_prices) / len(monthly_prices)

        return monthly_average / global_average
