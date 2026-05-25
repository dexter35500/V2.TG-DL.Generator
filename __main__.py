import os
import sys
import asyncio
import logging
from aiohttp import web

# Forzar directorio raíz en el PATH de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot import StreamBot
from vars import Var
from server import web_server

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def start_services():
    logging.info("Iniciando StreamBot de Telegram...")
    await StreamBot.start()
    
    # Configurar el servidor web de aiohttp
    app = web.Application()
    app.add_routes(web_server.routes)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render asigna el puerto dinámicamente en la variable PORT, si no usa 10000
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    logging.info(f"Servidor web corriendo en el puerto {port}")
    await site.start()
    
    # Mantener el loop corriendo indefinidamente
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        logging.info("Servidor detenido por el usuario.")
