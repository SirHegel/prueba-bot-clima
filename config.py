"""Configuracion del bot obtenida desde variables de entorno."""

import os


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Falta la variable de entorno obligatoria {name}."
        )
    return value


TELEGRAM_BOT_TOKEN = _required_env("TELEGRAM_BOT_TOKEN")
OPENWEATHER_API_KEY = _required_env("OPENWEATHER_API_KEY")
WEATHER_UNITS = os.getenv("WEATHER_UNITS", "metric")
WEATHER_LANG = os.getenv("WEATHER_LANG", "es")
