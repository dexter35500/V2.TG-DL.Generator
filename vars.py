from os import environ
from dotenv import load_dotenv

load_dotenv()

class Var(object):
    MULTI_CLIENT = False

    # --- CREDENCIALES ---
    API_ID = 21045233
    API_HASH = "862788c67926947605e55e4e69d0689b"
    BOT_TOKEN = "7538965042:AAHp2_yWvAn6yUvS-3XkQZ_2S_H63XkQZ_2"

    # --- IDENTIDAD Y PERMISOS ---
    OWNER_ID = 7233214534
    BIN_CHANNEL = -1002484080112
    UPDATES_CHANNEL = "Klan2500"

    # --- CONFIGURACIÓN DE RED ---
    PORT = 7860
    BIND_ADDRESS = "0.0.0.0"
    URL = "https://klan2500-direclinkgenbotv2.hf.space"

    # --- PARÁMETROS TÉCNICOS ---
    SLEEP_THRESHOLD = 60
    WORKERS = 6

    # --- LISTAS NEGRAS ---
    BANNED_CHANNELS = [-1001296894100]
    BANNED_USERS = [5275470552, 5287015877]
