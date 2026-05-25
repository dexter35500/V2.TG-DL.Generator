import os
import sys
import asyncio
import logging
from aiohttp import web

# Forzar la ruta raíz del proyecto en el PATH de Python para evitar errores de importación
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Importaciones absolutas unificadas
from bot.clients import StreamBot
from vars import Var
from server.stream_routes import routes

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def start_services():
    logging.info("Iniciando StreamBot de Telegram...")
    # Arranca el cliente de Pyrogram
    await StreamBot.start()
    
    # Configurar el servidor web de aiohttp para el streaming
    app = web.Application()
    app.add_routes(routes)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render asigna el puerto dinámicamente en la variable PORT (por defecto usa 10000)
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    logging.info(f"Servidor web de streaming escuchando en el puerto: {port}")
    await site.start()
    
    # Mantener el bucle asíncrono corriendo de por vida
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        logging.info("Servidor detenido manualmente.")
