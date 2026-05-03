from bot import StreamBot
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

@StreamBot.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply_text(
        text=f"Hola {message.from_user.mention},\n\nSoy un bot de Direct Links. Enviame cualquier archivo y te daré un enlace de streaming.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Canal de Actualizaciones", url="https://t.me/Klan2500")]]
        ),
        quote=True
    )