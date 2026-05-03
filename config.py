from os import environ
from dotenv import load_dotenv

load_dotenv()

class Var(object):
    MULTI_CLIENT = False
    API_ID = int(environ.get("API_ID", "TU_API_ID"))
    API_HASH = str(environ.get("API_HASH", "TU_API_HASH"))
    BOT_TOKEN = str(environ.get("BOT_TOKEN", "TU_BOT_TOKEN"))
    SLEEP_THRESHOLD = int(environ.get("SLEEP_THRESHOLD", "60"))
    WORKERS = int(environ.get("WORKERS", "6"))
    BIN_CHANNEL = int(environ.get("BIN_CHANNEL", "-100...")) # Tu ID de canal
    PORT = int(environ.get("PORT", 7860))
    BIND_ADDRESS = str(environ.get("WEB_SERVER_BIND_ADDRESS", "0.0.0.0"))
    URL = str(environ.get("URL", "https://klan2500-direclinkgenbot.hf.space"))
    OWNER_ID = int(environ.get('OWNER_ID', '7233214534'))