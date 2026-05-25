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

# Forzar la ruta raíz del proyecto en el PATH de Python para evitar errores de módulos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from bot.clients import StreamBot
from vars import Var

# Variable global que van a consumir las rutas de streaming para evitar importaciones circulares
bot_instance = None

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def start_services():
    global bot_instance
    logging.info("Inicializando instancias de Pyrogram...")
    
    # Instanciamos e iniciamos el bot dentro del bucle asíncrono
    bot_instance = StreamBot()
    await bot_instance.start()
    
    # Importación tardía de las rutas del servidor para evitar colisiones con la carga del bot
    from server.stream_routes import routes
    
    # Configurar el servidor web de aiohttp para el streaming de video/archivos
    app = web.Application()
    app.add_routes(routes)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render asigna el puerto de forma dinámica en la variable PORT (usa 10000 por defecto)
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    logging.info(f"Servidor web de streaming iniciado correctamente en el puerto: {port}")
    await site.start()
    
    # Bucle de mantenimiento permanente para sostener el servicio activo 24/7 en Render
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        logging.info("Servidor finalizado de forma manual por el usuario.")
