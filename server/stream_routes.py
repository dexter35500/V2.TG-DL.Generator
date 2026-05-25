import re
import logging
from aiohttp import web
from bot import StreamBot
from vars import Var
from utils.file_properties import get_file_ids

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(_):
    return web.json_response({"status": "running", "platform": "render_optimized"})

@routes.get(r"/{path:\S+}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        msg_id_match = re.search(r"(\d+)", path)
        if not msg_id_match:
            return web.Response(text="ID no encontrado", status=400)
            
        message_id = int(msg_id_match.group(1))
        secure_hash = request.rel_url.query.get("hash", "")

        # Si el navegador pide la interfaz visual (reproductor)
        if "Range" not in request.headers:
            from utils.render_template import render_page
            return web.Response(text=await render_page(message_id, secure_hash), content_type='text/html')
        
        # Si pide bytes, va al streamer
        return await media_streamer(request, message_id)
        
    except Exception as e:
        logging.error(f"Error en handler: {e}")
        return web.Response(text=f"Error: {str(e)}", status=500)

async def media_streamer(request, message_id):
    client = StreamBot 
    try:
        message = await client.get_messages(Var.BIN_CHANNEL, message_id)
        file_id = await get_file_ids(client, message)
    except Exception as e:
        return web.Response(text="Error de conexión con Telegram", status=502)
    
    if not file_id:
        return web.Response(text="Archivo no encontrado", status=404)
        
    file_size = getattr(file_id, "file_size", 0)
    range_header = request.headers.get("Range", "bytes=0-")
    
    try:
        start, end = range_header.replace("bytes=", "").split("-")
        from_bytes = int(start) if start else 0
        until_bytes = int(end) if end else file_size - 1
    except:
        from_bytes, until_bytes = 0, file_size - 1

    until_bytes = min(until_bytes, file_size - 1)
    chunk_length = until_bytes - from_bytes + 1

    response = web.StreamResponse(
        status=206,
        headers={
            "Content-Type": getattr(file_id, "mime_type", "video/mp4"),
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Length": str(chunk_length),
            "Accept-Ranges": "bytes",
            "Access-Control-Allow-Origin": "*",
            "Content-Disposition": f'inline; filename="{getattr(file_id, "file_name", "video.mp4")}"',
        }
    )

    await response.prepare(request)

    try:
        async for chunk in client.stream_media(file_id, offset=from_bytes, limit=chunk_length):
            if not chunk:
                break
            await response.write(chunk)
    except Exception as e:
        pass
    
    return response
