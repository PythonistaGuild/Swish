from __future__ import annotations

# stdlib
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
                web.get('/', self.websocket_handler),
                web.get('/search', self.search_tracks),
                web.get('/debug', self.debug_stats)
            ]
        )

        self.connections: dict[str, web.WebSocketResponse] = {}

    async def websocket_handler(self, request: web.Request) -> web.WebSocketResponse:

        logger.info(f'Received request to upgrade websocket from:: {request.remote}.')

        websocket = web.WebSocketResponse()
        await websocket.prepare(request)

        password = CONFIG['SERVER']['password']
        auth = request.headers.get('Authorization')

        if password != auth:
            logger.error(f'Authorization failed for request from:: {request.remote} with Authorization: {auth}')
            raise web.HTTPUnauthorized

        client_id = request.headers.get('Client-ID')
        if not client_id:
            logger.error('Unable to complete websocket handshake as your Client-ID header is missing.')
            raise web.HTTPBadRequest

        if not request.headers.get('User-Agent'):
            logger.warning('No User-Agent header provided. Please provide a User-Agent in future connections.')

        connection_id = str(uuid.uuid4())

        websocket['Client-ID'] = client_id
        websocket['Connection-ID'] = connection_id
        self.connections[connection_id] = websocket

        logger.info(f'Successful websocket handshake completed from:: {request.remote}.')

        async for message in websocket:  # type: aiohttp.WSMessage
            try:
                data = message.json()
            except Exception:
                logger.error(f'Unable to parse JSON from:: {request.remote}.')
                continue

            print(data)

        return websocket

    async def search_tracks(self):
        pass

    async def debug_stats(self):
        pass

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
