import math
from pyrogram import Client
from pyrogram.types import Message

async def get_file_ids(client: Client, message: Message):
    if message.document:
        return message.document
    if message.video:
        return message.video
    if message.audio:
        return message.audio
    return None

async def chunk_size(length):
    return 2 * 1024 * 1024 # 2MB chunks

async def offset_fix(offset, chunksize):
    return (offset // chunksize) * chunksize