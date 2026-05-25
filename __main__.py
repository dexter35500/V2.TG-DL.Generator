import os
import sys
import asyncio
import logging
from aiohttp import web

# Forzar la ruta raíz en el PATH de Python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from bot.clients import StreamBot
from vars import Var
from server.stream_routes import routes

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def start_services():
    logging.info("Inicializando instancias...")
    
    # Instanciamos y arrancamos el cliente directamente en el loop asíncrono
    bot_client = StreamBot()
    await bot_client.start()
    
    # Configurar el servidor web de aiohttp
    app = web.Application()
    app.add_routes(routes)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Puerto dinámico obligatorio para Render
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    logging.info(f"Servidor de streaming levantado en el puerto: {port}")
    await site.start()
    
    # Mantener el contenedor vivo las 24/7
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        logging.info("Servidor detenido por el usuario.")
