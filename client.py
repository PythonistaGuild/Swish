from __future__ import annotations

# stdlib
import asyncio

# packages
import aiohttp

# local
from src.config import CONFIG


URL = f'ws://{CONFIG["SERVER"]["host"]}:{CONFIG["SERVER"]["port"]}'
HEADERS = {
    'Authorization': CONFIG['SERVER']['password'],
    'User-Agent':    'swish-client v0.0.1a',
    'Client-Token':     "HUIDUIDaiuhd^bAbhjsa",
}
PAYLOAD = {
    'op': 'play',
    'd':  {
        'name': 'test'
    }
}


async def connect():

    session = aiohttp.ClientSession()
    websocket = await session.ws_connect(url=URL, headers=HEADERS, autoclose=False)
    print('WEBSOCKET: Connected')

    await websocket.send_json(PAYLOAD)
    print('WEBSOCKET: Sent example payload')

    while True:

        message = await websocket.receive()

        if message.type is aiohttp.WSMsgType.CLOSED:
            print('WEBSOCKET: Disconnected')
            break

        print(message)

    if not session.closed:
        await session.close()
    if not websocket.closed:
        await websocket.close()


try:
    asyncio.run(connect())
except KeyboardInterrupt:
    pass
