import os
import sys
import asyncio

# --- PARCHE DE COMPATIBILIDAD ASYNCIO PARA PYTHON 3.14+ ---
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

# Variable global para mitigar importaciones circulares en el servidor de rutas
bot_instance = None

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def start_services():
    global bot_instance
    logging.info("Inicializando instancias de Pyrogram...")
    
    # Instanciar e iniciar el bot de forma asíncrona
    bot_instance = StreamBot()
    await bot_instance.start()
    
    # Importación tardía controlada de las rutas para evitar colisiones
    from server.stream_routes import routes
    
    # Configurar el servidor web de aiohttp
    app = web.Application()
    app.add_routes(routes)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Puerto de Render asignado de forma dinámica
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    logging.info(f"Servidor web de streaming iniciado correctamente en el puerto: {port}")
    await site.start()
    
    # Bucle infinito para sostener el servicio activo 24/7
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        logging.info("Servidor finalizado por el usuario.")
