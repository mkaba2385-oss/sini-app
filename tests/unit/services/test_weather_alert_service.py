from sini.schemas.parcelle import CultureType, ParcelleResponse
from sini.schemas.user import RegionMali
from sini.services.weather import MeteoData, WeatherProvider
from sini.services.weather_alert_service import WeatherAlertService
from sini.strategies.alert_strategy import (
    DroughtAlertStrategy,
    RainAlertStrategy,
    WindAlertStrategy,
)


class FixedWeather(WeatherProvider):
    def __init__(self, data: MeteoData) -> None:
        self.data = data

    def get_meteo(self, region: str) -> MeteoData:
        return self.data


def make_parcelle() -> ParcelleResponse:
    from datetime import datetime, timezone

    return ParcelleResponse(
        id=1,
        name="Champ Test",
        superficie_ha=1.0,
        culture=CultureType.MAIS,
        region=RegionMali.SEGOU,
        owner_id=1,
        created_at=datetime.now(timezone.utc),
    )


def test_weather_alert_service_is_independent_from_real_api() -> None:
    service = WeatherAlertService(
        FixedWeather(MeteoData(temperature=38, humidite=20, alerte_secheresse=True)),
        DroughtAlertStrategy(),
    )
    assert service.generate_alert(make_parcelle()) is not None


def test_rain_and_wind_strategies() -> None:
    parcelle = make_parcelle()
    rain = RainAlertStrategy(rain_threshold_mm=40)
    wind = WindAlertStrategy(wind_threshold_kmh=50)
    assert rain.should_alert(
        parcelle, MeteoData(temperature=25, humidite=70, pluie_mm=45)
    )
    assert wind.should_alert(
        parcelle, MeteoData(temperature=25, humidite=70, vent_kmh=55)
    )
