from abc import ABC, abstractmethod

from sini.schemas.parcelle import ParcelleResponse
from sini.services.weather import MeteoData


class AlertStrategy(ABC):
    """Interface pour les stratégies de détection d'alertes."""

    @abstractmethod
    def should_alert(self, parcelle: ParcelleResponse, meteo: MeteoData) -> bool:
        pass

    @abstractmethod
    def build_message(self, parcelle: ParcelleResponse, meteo: MeteoData) -> str:
        pass


class DroughtAlertStrategy(AlertStrategy):
    """Stratégie d'alerte sur la sécheresse ou fortes températures."""

    def should_alert(self, parcelle: ParcelleResponse, meteo: MeteoData) -> bool:
        return meteo.alerte_secheresse or (
            meteo.temperature > 35.0 and meteo.humidite < 25.0
        )

    def build_message(self, parcelle: ParcelleResponse, meteo: MeteoData) -> str:
        region_str = (
            parcelle.region.value
            if hasattr(parcelle.region, "value")
            else str(parcelle.region)
        )
        return (
            f"Alerte sécheresse sur la parcelle {parcelle.name} ({region_str}) ! "
            f"Température : {meteo.temperature}°C."
        )


class HighTemperatureAlertStrategy(AlertStrategy):
    """Stratégie basée sur un seuil strict de température."""

    def __init__(self, temp_threshold: float = 40.0) -> None:
        self.temp_threshold = temp_threshold

    def should_alert(self, parcelle: ParcelleResponse, meteo: MeteoData) -> bool:
        return meteo.temperature >= self.temp_threshold

    def build_message(self, parcelle: ParcelleResponse, meteo: MeteoData) -> str:
        return (
            f"Alerte forte chaleur sur la parcelle {parcelle.name} ! "
            f"Seuil de {self.temp_threshold}°C dépassé ({meteo.temperature}°C)."
        )
