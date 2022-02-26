import asyncio

import aiohttp


async def main():

    headers = {'Authorization': 'helloworld!'}

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('ws://127.0.0.1:3555', headers=headers) as websocket:
            await websocket.send_str('Hello World!')


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
