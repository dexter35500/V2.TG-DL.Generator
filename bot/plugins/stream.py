import logging
from bot import StreamBot
from vars import Var
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.file_properties import get_file_ids
from utils.human_readable import humanbytes

@StreamBot.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def stream_handler(client: StreamBot, message: Message):
    try:
        # Reenvío automático al canal de log (BIN_CHANNEL)
        log_msg = await message.forward(chat_id=Var.BIN_CHANNEL)
        
        file_id = await get_file_ids(client, message)
        file_name = file_id.file_name.replace("_", " ")
        file_size = humanbytes(file_id.file_size)
        
        # Hash basado en el unique_id
        secure_hash = file_id.unique_id[:6]
        
        # Usamos el message.id del mensaje reenviado al canal para el enlace permanente
        stream_link = f"{Var.URL}/{log_msg.id}?hash={secure_hash}"
        watch_link = f"{Var.URL}/watch/{log_msg.id}?hash={secure_hash}"

        msg_text = (
            "**📦 Archivo Procesado**\n\n"
            f"**Nombre:** `{file_name}`\n"
            f"**Tamaño:** `{file_size}`\n\n"
            f"**Enlace de descarga:**\n`{stream_link}`"
        )

        await message.reply_text(
            text=msg_text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Reproducir Online 📺", url=watch_link)],
                    [InlineKeyboardButton("Descargar 📥", url=stream_link)]
                ]
            ),
            quote=True
        )
    except Exception as e:
        logging.error(e, exc_info=True)
        await message.reply_text(f"Error: {e}")