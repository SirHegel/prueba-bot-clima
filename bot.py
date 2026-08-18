"""Bot de Telegram para consultar el clima actual de una ciudad."""

import asyncio

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import TELEGRAM_BOT_TOKEN, WEATHER_UNITS
from weather import CityNotFound, WeatherServiceError, get_weather


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Da la bienvenida y explica brevemente como usar el bot."""
    if update.effective_message:
        await update.effective_message.reply_text(
            "👋 ¡Hola! Soy tu bot del clima.\n\n"
            "Envíame el nombre de una ciudad o usa /clima <ciudad> "
            "para consultar el tiempo actual."
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Muestra los comandos disponibles."""
    if update.effective_message:
        await update.effective_message.reply_text(
            "Comandos disponibles:\n"
            "/start - Mostrar el mensaje de bienvenida\n"
            "/help - Mostrar esta ayuda\n"
            "/clima <ciudad> - Consultar el clima de una ciudad\n\n"
            "También puedes enviarme directamente el nombre de una ciudad."
        )


def _unit_labels() -> tuple[str, str]:
    """Devuelve las unidades de temperatura y viento configuradas."""
    if WEATHER_UNITS == "imperial":
        return "°F", "mph"
    if WEATHER_UNITS == "standard":
        return "K", "m/s"
    return "°C", "m/s"


async def _send_weather(update: Update, city: str) -> None:
    """Consulta y envia el clima, traduciendo errores a mensajes amigables."""
    message = update.effective_message
    if not message:
        return

    city = city.strip()
    if not city:
        await message.reply_text("🏙️ Por favor, indica una ciudad.")
        return

    try:
        weather = await asyncio.to_thread(get_weather, city)
    except CityNotFound:
        await message.reply_text(
            f"🔎 No encontré la ciudad «{city}». Revisa el nombre e inténtalo de nuevo."
        )
        return
    except WeatherServiceError:
        await message.reply_text(
            "⚠️ No pude consultar el clima en este momento. Inténtalo de nuevo más tarde."
        )
        return

    temperature_unit, wind_unit = _unit_labels()
    await message.reply_text(
        f"🏙️ Ciudad: {weather['city']}\n"
        f"🌍 País: {weather['country']}\n"
        f"☁️ Descripción: {weather['description'].capitalize()}\n"
        f"🌡️ Temperatura: {weather['temp']} {temperature_unit}\n"
        f"🤗 Sensación térmica: {weather['feels_like']} {temperature_unit}\n"
        f"💧 Humedad: {weather['humidity']}%\n"
        f"💨 Viento: {weather['wind_speed']} {wind_unit}"
    )


async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Consulta el clima de la ciudad recibida como argumento."""
    await _send_weather(update, " ".join(context.args))


async def city_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Trata cualquier mensaje de texto libre como el nombre de una ciudad."""
    if update.effective_message and update.effective_message.text:
        await _send_weather(update, update.effective_message.text)


def main() -> None:
    """Configura los handlers e inicia el bot mediante polling."""
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clima", clima))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, city_text))

    application.run_polling()


if __name__ == "__main__":
    main()
