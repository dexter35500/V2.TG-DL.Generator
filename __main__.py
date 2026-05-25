import os
import sys
import asyncio
import logging
from aiohttp import web

# FORZAR RUTA ABSOLUTA DEL SISTEMA (Solución para Python 3.14+)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Ahora sí realizamos las importaciones con la ruta inyectada
from bot.clients import StreamBot
from vars import Var
from server.stream_routes import routes

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def start_services():
    logging.info("Iniciando StreamBot de Telegram...")
    await StreamBot.start()
    
    # Inicializar el servidor web asíncrono
    app = web.Application()
    app.add_routes(routes)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render asigna el puerto dinámicamente en la variable PORT
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    logging.info(f"Servidor web corriendo en el puerto {port}")
    await site.start()
    
    # Mantener el bucle infinito para que el contenedor no muera
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        logging.info("Servidor detenido.")
