import os
from dotenv import load_dotenv

# Cargamos el archivo .env local si es que existe (útil por si probás el código en tu PC)
if os.path.exists("config.env"):
    load_dotenv("config.env")

class Var(object):
    MULTI_CLIENT = False

    # Credenciales de la API de Telegram (Se obtienen de my.telegram.org)
    API_ID = int(os.environ.get("API_ID", 30353560))
    API_HASH = os.environ.get("API_HASH", "72d07df770966e36c30af10d24ff3404")
    
    # Token de tu Bot (Te lo da @BotFather)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8770613427:AAGw-aBT2Jz4zPDpwtmpXrAt8d6TBpbu410")
    
    # Tu ID de usuario de Telegram (para comandos de administración si tuvieras)
    OWNER_ID = int(os.environ.get("OWNER_ID", 5064367463))
    
    # ID del canal de almacenamiento (Debe empezar con -100)
    BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", -1003812620810))
    
    # Nombre de usuario de tu canal de novedades o grupo (sin el @)
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "democracia_filmica")

    # --- CONFIGURACIÓN DE RED PARA RENDER ---
    # Render asigna automáticamente el puerto en la variable 'PORT'. Si no existe, usa el 10000.
    PORT = int(os.environ.get("PORT", 10000))
    BIND_ADDRESS = "0.0.0.0"
    
    # El enlace público de tu servicio en Render (sirve para estructurar las URLs de streaming)
    URL = os.environ.get("URL", "https://direclinkgen-botv2.onrender.com")

    # Ajustes de rendimiento y seguridad de Pyrogram
    SLEEP_THRESHOLD = 60
    WORKERS = 6
    BANNED_CHANNELS = [-1001296894100]
    BANNED_USERS = [5275470552, 5287015877]
