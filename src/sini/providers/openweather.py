import httpx

from sini.services.weather import MeteoData, WeatherProvider


class OpenWeatherMapProvider(WeatherProvider):
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.openweathermap.org/data/2.5/weather",
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url

    def get_meteo(self, region: str) -> MeteoData:
        params = {
            "q": f"{region},ML",
            "appid": self.api_key,
            "units": "metric",
        }

        response = httpx.get(
            self.base_url,
            params=params,
            timeout=10.0,
        )

        response.raise_for_status()

        data = response.json()

        temperature = data["main"]["temp"]
        humidite = data["main"]["humidity"]

        vent_ms = data.get("wind", {}).get("speed", 0.0)
        vent_kmh = vent_ms * 3.6

        pluie_mm = data.get("rain", {}).get("1h", 0.0)

        return MeteoData(
            temperature=temperature,
            humidite=humidite,
            pluie_mm=pluie_mm,
            vent_kmh=vent_kmh,
        )
