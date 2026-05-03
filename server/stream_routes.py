import re
import time
import math
import logging
import mimetypes
from aiohttp import web
from bot.clients import multi_clients, work_loads
from bot import StreamBot
from server.exceptions import FIleNotFound, InvalidHash
from vars import Var
import utils
from utils.render_template import render_page

try:
    from __main__ import StartTime, __version__
except ImportError:
    StartTime = time.time()
    __version__ = "1.0.0"

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(_):
    return web.json_response(
        {
            "server_status": "running",
            "uptime": utils.get_readable_time(time.time() - StartTime),
            "telegram_bot": "@" + StreamBot.username if StreamBot.username else "Bot",
            "connected_bots": len(multi_clients),
            "version": __version__,
        }
    )

@routes.get(r"/watch/{path:\S+}", allow_head=True)
async def watch_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if match:
            secure_hash = match.group(1)
            message_id = int(match.group(2))
        else:
            message_id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")
        return web.Response(text=await render_page(message_id, secure_hash), content_type='text/html')
    except Exception as e:
        raise web.HTTPInternalServerError(text=str(e))

@routes.get(r"/{path:\S+}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if match:
            secure_hash = match.group(1)
            message_id = int(match.group(2))
        else:
            message_id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")
        return await media_streamer(request, message_id, secure_hash)
    except Exception as e:
        raise web.HTTPInternalServerError(text=str(e))

async def media_streamer(request, message_id, secure_hash):
    range_header = request.headers.get("Range", 0)
    index = min(work_loads, key=work_loads.get)
    faster_client = multi_clients[index]
    tg_connect = utils.ByteStreamer(faster_client)

    file_id = await tg_connect.get_file_properties(message_id)
    if file_id.unique_id[:6] != secure_hash:
        raise web.HTTPForbidden(text="Hash inválido")

    file_size = file_id.file_size
    if range_header:
        from_bytes, until_bytes = range_header.replace("bytes=", "").split("-")
        from_bytes = int(from_bytes)
        until_bytes = int(until_bytes) if until_bytes else file_size - 1
    else:
        from_bytes, until_bytes = 0, file_size - 1

    req_length = until_bytes - from_bytes
    new_chunk_size = await utils.chunk_size(req_length)
    offset = await utils.offset_fix(from_bytes, new_chunk_size)
    body = tg_connect.yield_file(file_id, index, offset, from_bytes - offset, (until_bytes % new_chunk_size) + 1, math.ceil(req_length / new_chunk_size), new_chunk_size)

    mime_type = file_id.mime_type or "application/octet-stream"
    return web.Response(
        status=206 if range_header else 200,
        body=body,
        headers={
            "Content-Type": mime_type,
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Disposition": f'inline; filename="{file_id.file_name}"',
            "Accept-Ranges": "bytes",
        }
    )
