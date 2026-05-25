import os
import sys
import asyncio

# --- PARCHE DE COMPATIBILIDAD ASYNCIO PARA PYTHON 3.14+ ---
# Forzamos la creación de un bucle de eventos en el hilo principal antes de importar Pyrogram
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

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
    logging.info("Inicializando instancias de red...")
    
    # Arrancar el cliente de Pyrogram de forma asíncrona limpia
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
    
    logging.info(f"Servidor de streaming levantado con éxito en el puerto: {port}")
    await site.start()
    
    # Mantener el contenedor de Render vivo las 24/7
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        logging.info("Servidor detenido por el usuario.")
