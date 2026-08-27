from unittest.mock import Mock, patch

import httpx
import pytest

from sini.providers.openweather import OpenWeatherMapProvider


def test_get_meteo_returns_meteo_data() -> None:
    provider = OpenWeatherMapProvider(
        api_key="fake-api-key",
    )

    fake_response = Mock()

    fake_response.json.return_value = {
        "main": {
            "temp": 38.5,
            "humidity": 20,
        },
        "wind": {
            "speed": 5.0,
        },
        "rain": {
            "1h": 2.5,
        },
    }

    with patch(
        "sini.providers.openweather.httpx.get",
        return_value=fake_response,
    ):
        meteo = provider.get_meteo("Kayes")

    assert meteo.temperature == 38.5
    assert meteo.humidite == 20
    assert meteo.pluie_mm == 2.5

    # 5 m/s × 3.6 = 18 km/h
    assert meteo.vent_kmh == 18.0

    assert meteo.alerte_secheresse is False


def test_get_meteo_without_rain() -> None:
    provider = OpenWeatherMapProvider(
        api_key="fake-api-key",
    )

    fake_response = Mock()

    fake_response.json.return_value = {
        "main": {
            "temp": 40.0,
            "humidity": 25,
        },
        "wind": {
            "speed": 3.0,
        },
    }

    with patch(
        "sini.providers.openweather.httpx.get",
        return_value=fake_response,
    ):
        meteo = provider.get_meteo("Gao")

    assert meteo.temperature == 40.0
    assert meteo.humidite == 25
    assert meteo.pluie_mm == 0.0

    # 3 m/s × 3.6 = 10.8 km/h
    assert meteo.vent_kmh == 10.8

    assert meteo.alerte_secheresse is False


def test_get_meteo_without_wind() -> None:
    provider = OpenWeatherMapProvider(
        api_key="fake-api-key",
    )

    fake_response = Mock()

    fake_response.json.return_value = {
        "main": {
            "temp": 35.0,
            "humidity": 60,
        },
        "rain": {
            "1h": 1.5,
        },
    }

    with patch(
        "sini.providers.openweather.httpx.get",
        return_value=fake_response,
    ):
        meteo = provider.get_meteo("Bamako")

    assert meteo.temperature == 35.0
    assert meteo.humidite == 60
    assert meteo.pluie_mm == 1.5
    assert meteo.vent_kmh == 0.0
    assert meteo.alerte_secheresse is False


def test_get_meteo_raises_http_error() -> None:
    provider = OpenWeatherMapProvider(
        api_key="invalid-api-key",
    )

    fake_response = Mock()

    fake_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Invalid API key",
        request=Mock(),
        response=Mock(),
    )

    with (
        patch(
            "sini.providers.openweather.httpx.get",
            return_value=fake_response,
        ),
        pytest.raises(httpx.HTTPStatusError),
    ):
        provider.get_meteo("Kayes")
