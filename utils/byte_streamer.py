from pyrogram import Client

class ByteStreamer:
    def __init__(self, client: Client):
        self.client = client

    async def get_file_properties(self, message_id):
        from vars import Var
        msg = await self.client.get_messages(Var.BIN_CHANNEL, message_id)
        return await get_file_ids(self.client, msg)

    async def yield_file(self, file_id, index, offset, first_part, last_part, total_parts, chunk_size):
        async for chunk in self.client.stream_media(file_id, offset=offset):
            yield chunk