from __future__ import annotations

# stdlib
import asyncio

# packages
import aiohttp

# local
from src.config import CONFIG


async def connect():
    url = f'ws://{CONFIG["SERVER"]["host"]}:{CONFIG["SERVER"]["port"]}'
    headers = {
        'Authorization': CONFIG['SERVER']['password'], 'User-Agent': 'swish-client v0.0.1a', 'Client-ID': 00000,
    }

    session = aiohttp.ClientSession()
    websocket = await session.ws_connect(url=url, headers=headers, autoclose=False)
    print('WEBSOCKET: Connected')

    await websocket.send_json(
        {
            "op": "play",
            "d":  {
                "name": "test"
            }
        }
    )

    await websocket.close()
    await session.close()
    print('WEBSOCKET: Disconnected')


try:
    asyncio.run(connect())
except KeyboardInterrupt:
    pass
