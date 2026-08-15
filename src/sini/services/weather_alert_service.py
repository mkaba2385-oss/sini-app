from sini.schemas.parcelle import ParcelleResponse
from sini.services.weather import MeteoData, WeatherProvider
from sini.strategies.alert_strategy import AlertStrategy


class WeatherAlertService:
    """Génère des alertes météo sans dépendre d'une API météo concrète."""

    def __init__(
        self, weather_provider: WeatherProvider, strategy: AlertStrategy
    ) -> None:
        self.weather_provider = weather_provider
        self.strategy = strategy

    def generate_alert(self, parcelle: ParcelleResponse) -> str | None:
        """Retourne le message d'alerte si la météo déclenche la stratégie."""
        region = (
            parcelle.region.value
            if hasattr(parcelle.region, "value")
            else str(parcelle.region)
        )
        meteo: MeteoData = self.weather_provider.get_meteo(region)
        if not self.strategy.should_alert(parcelle, meteo):
            return None
        return self.strategy.build_message(parcelle, meteo)
