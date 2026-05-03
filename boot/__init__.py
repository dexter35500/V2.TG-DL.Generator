from pyrogram import Client
from vars import Var
from bot.clients import multi_clients, work_loads

StreamBot = Client(
    name="StreamBot",
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    bot_token=Var.BOT_TOKEN,
    sleep_threshold=Var.SLEEP_THRESHOLD,
    plugins={"root": "bot/plugins"}
)