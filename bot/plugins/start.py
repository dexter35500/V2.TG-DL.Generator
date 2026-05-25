import logging
from pyrogram import filters
from pyrogram.types import Message
from vars import Var

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@filters.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    # Usamos "client" directamente (que es tu StreamBot corriendo)
    logging.info(f"Comando /start recibido de {message.from_user.id}")
    
    await message.reply_text(
        text=f"¡Hola {message.from_user.mention}!\n\n"
             f"Soy un bot de streaming de alta velocidad para Render.\n"
             f"Enviame un archivo de mi canal de almacenamiento para generar tu enlace dinámico.",
        disable_web_page_preview=True
    )
