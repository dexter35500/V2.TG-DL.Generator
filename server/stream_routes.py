import os
import re
import logging
from aiohttp import web
from vars import Var

# Importamos directamente la clase para evitar el bucle de importación circular
from bot.clients import StreamBot

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(_):
    return web.json_response({
        "server_status": "running",
        "bot_username": "StreamBot",
        "version": "2.0.0"
    })

@routes.get(r"/{path:\S+}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        msg_id_match = re.search(r"(\d+)", path)
        if not msg_id_match:
            return web.Response(text="ID de mensaje inválido o no encontrado", status=400)
            
        message_id = int(msg_id_match.group(1))
        
        # Accedemos a la instancia global a través del estado de la aplicación o directa
        from __main__ import bot_instance
        if not bot_instance:
            return web.Response(text="El cliente del Bot no está inicializado", status=503)

        message = await bot_instance.get_messages(Var.BIN_CHANNEL, message_id)
        
        file_id = None
        for attr in ["video", "document", "audio"]:
            if getattr(message, attr, None):
                file_id = getattr(message, attr)
                break
                
        if not file_id:
            return web.Response(text="El mensaje no contiene un archivo válido", status=404)

        file_size = getattr(file_id, "file_size", 0)
        range_header = request.headers.get("Range", "bytes=0-")
        
        try:
            start, end = range_header.replace("bytes=", "").split("-")
            from_bytes = int(start) if start else 0
            until_bytes = int(end) if end else file_size - 1
        except Exception:
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
        
        async for chunk in bot_instance.stream_media(file_id, offset=from_bytes, limit=chunk_length):
            if not chunk:
                break
            await response.write(chunk)
            
        return response
    except Exception as e:
        logging.error(f"Error en el streaming de rutas: {str(e)}")
        return web.Response(text=f"Error interno: {str(e)}", status=500)
