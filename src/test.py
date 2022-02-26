from __future__ import annotations

# stdlib
import asyncio

# packages
import aiohttp


async def main():

    headers = {'Authorization': 'helloworld!', 'Client-ID': "1234"}

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('ws://127.0.0.1:3555', headers=headers) as websocket:
            while True:
                await asyncio.sleep(30)
                await websocket.send_str('PING')


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
