import os

class Var(object):
    MULTI_CLIENT = False

    # Credenciales del panel de Render
    API_ID = int(os.environ.get("API_ID", 30353560))
    API_HASH = os.environ.get("API_HASH", "72d07df770966e36c30af10d24ff3404")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8770613427:AAGw-aBT2Jz4zPDpwtmpXrAt8d6TBpbu410")
    OWNER_ID = int(os.environ.get("OWNER_ID", 5064367463))
    
    # Canales de Telegram
    BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", -1003812620810))
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "democracia_filmica")

    # Mapeo de red para el contenedor de Render
    PORT = int(os.environ.get("PORT", 10000))
    BIND_ADDRESS = "0.0.0.0"
    URL = os.environ.get("URL", "https://direclinkgen-botv2.onrender.com")

    # Ajustes internos de Pyrogram
    SLEEP_THRESHOLD = 60
    WORKERS = 6
    BANNED_CHANNELS = [-1001296894100]
    BANNED_USERS = [5275470552, 5287015877]
