import aiohttp
import asyncio
from vars import Var
from utils.human_readable import humanbytes

async def render_page(message_id, secure_hash):
    # Generamos el enlace directo que el reproductor usará
    src = f"{Var.URL}/{message_id}?hash={secure_hash}"

    # HTML del reproductor (usando el estándar Plyr para que se vea profesional)
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stream Player - DirecLinkGenV2</title>
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <style>
        body {{
            margin: 0;
            background: #000;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            font-family: sans-serif;
        }}
        .container {{
            width: 100%;
            max-width: 900px;
        }}
        .info {{
            color: #fff;
            text-align: center;
            padding: 20px;
        }}
        a {{
            color: #00b3ff;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <video id="player" playsinline controls data-poster="">
            <source src="{src}" type="video/mp4" />
        </video>
        <div class="info">
            <p>Si el video no carga, intenta <a href="{src}">descargarlo directamente aquí</a>.</p>
        </div>
    </div>

    <script src="https://cdn.plyr.io/3.7.8/plyr.js"></script>
    <script>
        const player = new Plyr('#player');
    </script>
</body>
</html>
"""
