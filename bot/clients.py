import logging
from pyrogram import Client
from vars import Var

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class StreamBot(Client):
    def __init__(self):
        super().__init__(
            name="StreamBot",
            api_id=Var.API_ID,
            api_hash=Var.API_HASH,
            bot_token=Var.BOT_TOKEN,
            workers=Var.WORKERS,
            plugins=dict(root="bot/plugins")
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        logging.info(f"¡Bot @{me.username} iniciado con éxito!")

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot detenido.")
