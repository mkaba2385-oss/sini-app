from abc import ABC, abstractmethod

from sini.schemas.parcelle import ParcelleResponse
from sini.services.weather import MeteoData


class AlertStrategy(ABC):
    """Interface commune des stratégies d'alertes météo."""

    @abstractmethod
    def should_alert(self, parcelle: ParcelleResponse, meteo: MeteoData) -> bool:
        """Indique si les conditions météo déclenchent une alerte."""
        raise NotImplementedError

    @abstractmethod
    def build_message(self, parcelle: ParcelleResponse, meteo: MeteoData) -> str:
        """Construit le message d'alerte."""
        raise NotImplementedError


class RainAlertStrategy(AlertStrategy):
    """Alerte en cas de fortes précipitations."""

    def __init__(self, rain_threshold_mm: float = 40.0) -> None:
        self.rain_threshold_mm = rain_threshold_mm

    def should_alert(self, parcelle: ParcelleResponse, meteo: MeteoData) -> bool:
        return getattr(meteo, "pluie_mm", 0.0) >= self.rain_threshold_mm

    def build_message(self, parcelle: ParcelleResponse, meteo: MeteoData) -> str:
        return (
            f"Alerte fortes pluies sur la parcelle {parcelle.name} : "
            f"{getattr(meteo, 'pluie_mm', 0.0)} mm."
        )


class DroughtAlertStrategy(AlertStrategy):
    """Alerte en cas de sécheresse ou de forte chaleur sèche."""

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


class WindAlertStrategy(AlertStrategy):
    """Alerte en cas de vent fort."""

    def __init__(self, wind_threshold_kmh: float = 60.0) -> None:
        self.wind_threshold_kmh = wind_threshold_kmh

    def should_alert(self, parcelle: ParcelleResponse, meteo: MeteoData) -> bool:
        return getattr(meteo, "vent_kmh", 0.0) >= self.wind_threshold_kmh

    def build_message(self, parcelle: ParcelleResponse, meteo: MeteoData) -> str:
        return (
            f"Alerte vent fort sur la parcelle {parcelle.name} : "
            f"{getattr(meteo, 'vent_kmh', 0.0)} km/h."
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
