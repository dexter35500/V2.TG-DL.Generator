import logging
from vars import Var

logging.getLogger("pyrogram").setLevel(logging.WARNING)
multi_clients = {}
work_loads = {}

async def initialize_clients():
    from bot import StreamBot
    multi_clients[0] = StreamBot
    work_loads[0] = 0
    logging.info("Clientes inicializados correctamente.")