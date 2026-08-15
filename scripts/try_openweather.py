import os

import requests

# Coordonnées par défaut : Bamako, Mali
LATITUDE = 12.6392
LONGITUDE = -8.0029


def fetch_weather():
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        print("Erreur : OPENWEATHER_API_KEY n'est pas définie.")
        print(
            "Exemple : OPENWEATHER_API_KEY=votre_cle python scripts/try_openweather.py"
        )

        return

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": LATITUDE,
        "lon": LONGITUDE,
        "appid": api_key,
        "units": "metric",
        "lang": "fr",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        print("--- Appel OpenWeather Réussi ---")
        print(f"Ville / Zone : {data.get('name', 'N/A')}")
        print(f"Température : {data['main']['temp']} °C")
        print(f"Météo : {data['weather'][0]['description'].capitalize()}")
        print(f"Humidité : {data['main']['humidity']} %")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête API OpenWeather : {e}")


if __name__ == "__main__":
    fetch_weather()
