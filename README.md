# Bot Clima Telegram

Bot de Telegram escrito en Python que consulta el clima actual de una ciudad mediante la API de OpenWeatherMap. Puedes enviar el nombre de una ciudad como texto o utilizar el comando `/clima`.

## Requisitos

- Python 3.10 o superior.
- Una cuenta de Telegram.
- Una cuenta de OpenWeatherMap.

## Credenciales

### Token de Telegram con BotFather

1. Abre Telegram y busca el bot oficial [@BotFather](https://t.me/BotFather).
2. Inicia la conversación y envía `/newbot`.
3. Indica el nombre visible y un nombre de usuario para el bot. El nombre de usuario debe terminar en `bot`.
4. Copia el token que entrega BotFather y úsalo como valor de `TELEGRAM_BOT_TOKEN`.

No publiques el token ni lo incluyas en el control de versiones. Si se filtra, utiliza `/revoke` en BotFather para reemplazarlo.

### API key de OpenWeatherMap

1. Crea una cuenta en [OpenWeatherMap](https://openweathermap.org/).
2. Abre la sección **My API keys** de tu perfil.
3. Genera una API key o copia la clave predeterminada.
4. Úsala como valor de `OPENWEATHER_API_KEY`.

Una clave nueva puede tardar un tiempo en activarse.

## Variables de entorno

| Variable | Obligatoria | Valor predeterminado | Descripción |
| --- | --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Sí | Ninguno | Token generado por BotFather. |
| `OPENWEATHER_API_KEY` | Sí | Ninguno | Clave para consultar la API de OpenWeatherMap. |
| `WEATHER_UNITS` | No | `metric` | Sistema de unidades: `metric`, `imperial` o `standard`. |
| `WEATHER_LANG` | No | `es` | Código del idioma usado en la descripción del clima. |

## Instalación

Desde la carpeta del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edita `.env` y rellena al menos `TELEGRAM_BOT_TOKEN` y `OPENWEATHER_API_KEY`. La aplicación obtiene la configuración del entorno del proceso, por lo que debes cargar el archivo en la terminal antes de ejecutarla:

```bash
set -a
source .env
set +a
```

En Windows PowerShell, define las mismas variables con `$env:NOMBRE="valor"` antes de iniciar el bot.

## Ejecución

Con el entorno virtual activo y las variables de entorno cargadas:

```bash
python bot.py
```

El bot se mantiene en ejecución mediante *polling*. Para detenerlo, presiona `Ctrl+C`.

## Comandos y uso

- `/start`: muestra el mensaje de bienvenida. Ejemplo: `/start`.
- `/help`: muestra la ayuda y los comandos disponibles. Ejemplo: `/help`.
- `/clima <ciudad>`: consulta el clima actual. Ejemplos: `/clima Bogotá` o `/clima New York`.
- Texto libre: cualquier mensaje que no sea un comando se interpreta como una ciudad. Ejemplo: `Medellín`.

## Estructura del proyecto

```text
bot-clima/
├── config.py          # Lee y valida la configuración del entorno.
├── weather.py         # Consulta y normaliza los datos de OpenWeatherMap.
├── bot.py             # Configura Telegram y maneja comandos y mensajes.
├── requirements.txt   # Dependencias de Python.
├── .env.example       # Plantilla de variables de entorno.
├── .gitignore         # Excluye credenciales y archivos generados.
└── README.md          # Documentación de instalación y uso.
```

## Solución de problemas

- **Token inválido:** verifica que `TELEGRAM_BOT_TOKEN` coincida exactamente con el token de BotFather, sin espacios ni comillas innecesarias. Si fue revocado, copia el token nuevo y vuelve a cargar las variables.
- **Ciudad no encontrada:** revisa la ortografía, agrega el país para evitar ambigüedades (por ejemplo, `/clima Córdoba, AR`) o prueba el nombre internacional de la ciudad.
- **API key sin activar:** una clave nueva de OpenWeatherMap puede no funcionar inmediatamente. Espera a que se active, confirma que `OPENWEATHER_API_KEY` esté bien escrita y vuelve a iniciar el bot.
