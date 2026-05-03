import asyncio
import logging
import time
from bot import StreamBot
from server import web_server
from aiohttp import web
from vars import Var
from bot.clients import initialize_clients

logging.basicConfig(level=logging.INFO)
StartTime = time.time()

async def start_services():
    print("--- INICIANDO SERVICIOS ---")
    await StreamBot.start()
    await initialize_clients()
    
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, Var.PORT).start()
    
    print(f"--- BOT Y SERVIDOR EN PUERTO {Var.PORT} ---")
    from pyrogram import idle
    await idle()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_services())