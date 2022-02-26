from __future__ import annotations

# stdlib
import asyncio
import logging
import uuid

# packages
import aiohttp
from aiohttp import web

# local
from .config import CONFIG


logger = logging.getLogger('swish')


class Server(web.Application):

    def __init__(self):
        super().__init__()

        self.add_routes(
            [
                web.get('/', self.websocket_handler)
            ]
        )

        self.websockets = {}

    async def websocket_handler(self, request: web.Request):
        logger.info(f'Received request to upgrade websocket from:: {request.remote}.')

        ws = web.WebSocketResponse()
        await ws.prepare(request)

        password = CONFIG['SERVER']['password']
        auth = request.headers.get('Authorization')

        if password != auth:
            logger.error(f'Authorization failed for request from:: {request.remote} with Authorization: {auth}')
            raise web.HTTPUnauthorized

        if not request.headers.get('Client-ID'):
            logger.error('Unable to compleeete websocket handshake as your Client-ID header is missing.')
            raise web.HTTPBadRequest

        if not request.headers.get('User-Agent'):
            logger.warn('No User-Agent header provided. Please provide a User-Agent in future connections.')

        UUID = uuid.uuid4()
        self.websockets[UUID] = {'websocket': ws, 'headers': request.headers}

        logger.info(f'Successful websocket handshake completed from:: {request.remote}.')

        async for message in ws:
            message: aiohttp.WSMessage
            print(message.data)

    async def _run_app(self):
        host_ = CONFIG['SERVER']['host']
        port_ = CONFIG['SERVER']['port']

        logger.info(f'Starting Swish server on {host_}:{port_}...')

        runner = web.AppRunner(app=self)
        await runner.setup()

        site = web.TCPSite(
            runner=runner,
            host=host_,
            port=port_
        )

        await site.start()
        logger.info('Successfully started swish server...')
