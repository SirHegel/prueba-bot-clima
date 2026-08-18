"""Cliente simple para consultar el clima actual en OpenWeatherMap."""

from typing import Any

import requests

from config import OPENWEATHER_API_KEY, WEATHER_LANG, WEATHER_UNITS


OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


class CityNotFound(Exception):
    """Indica que OpenWeatherMap no encontro la ciudad solicitada."""


class WeatherServiceError(Exception):
    """Indica un fallo de red o una respuesta invalida del servicio de clima."""


def get_weather(city: str) -> dict[str, Any]:
    """Obtiene y normaliza el clima actual de una ciudad."""
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": WEATHER_UNITS,
        "lang": WEATHER_LANG,
    }

    try:
        response = requests.get(OPENWEATHER_URL, params=params, timeout=10)
    except requests.RequestException as exc:
        raise WeatherServiceError("No se pudo conectar con el servicio de clima.") from exc

    if response.status_code == 404:
        raise CityNotFound(f"No se encontro la ciudad: {city}")

    try:
        response.raise_for_status()
        data = response.json()
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "description": data["weather"][0]["description"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError) as exc:
        raise WeatherServiceError("El servicio de clima devolvio una respuesta invalida.") from exc
