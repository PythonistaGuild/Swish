from __future__ import annotations

# stdlib
import logging
import uuid

# packages
import aiohttp
import aiohttp.web

# local
from .config import CONFIG
from .ip_rotator import IpRotator
from .player import Player
from .search import Search


logger: logging.Logger = logging.getLogger('swish.server')


class Server(aiohttp.web.Application):

    def __init__(self):
        super().__init__()

        self.rotator: IpRotator = IpRotator()
        self.search: Search = Search()

        self.add_routes(
            [
                aiohttp.web.get('/', self.websocket_handler),
                aiohttp.web.get('/search', self.search_tracks),
                aiohttp.web.get('/debug', self.debug_stats)
            ]
        )

        self.connections: dict[str, aiohttp.web.WebSocketResponse] = {}

    async def _run_app(self) -> None:

        logger.debug('Starting Swish server...')

        host = CONFIG['SERVER']['host']
        port = CONFIG['SERVER']['port']

        runner = aiohttp.web.AppRunner(app=self)
        await runner.setup()

        site = aiohttp.web.TCPSite(
            runner=runner,
            host=host,
            port=port
        )
        await site.start()

        logger.info(f'Swish server started on {host}:{port}')

    async def websocket_handler(self, request: aiohttp.web.Request) -> aiohttp.web.WebSocketResponse:

        logger.info(f'Incoming websocket connection request from "{request.remote}".')

        websocket = aiohttp.web.WebSocketResponse()
        await websocket.prepare(request)

        # User-Agent
        user_agent = request.headers.get('User-Agent')

        if not user_agent:
            logger.error(f'Websocket connection from "{request.remote}" failed due to missing User-Agent header.')
            await websocket.close(code=4000, message=b'Missing "User-Agent" header.')
            return websocket

        client_name = f'{user_agent} ({request.remote})'

        # User-Id
        user_id = request.headers.get('User-Id')

        if not user_id:
            logger.error(f'Websocket connection from "{request.remote}" failed due to missing User-Id header.')
            await websocket.close(code=4000, message=b'Missing "User-Id" header.')
            return websocket

        # Authorization
        authorization = request.headers.get('Authorization')

        if CONFIG['SERVER']['password'] != authorization:
            logger.error(f'Websocket connection from <{client_name}> failed due to mismatched Authorization header: {authorization}')
            await websocket.close(code=4001, message=b'Authorization failed.')
            return websocket

        # Finalise connection
        websocket['user_agent'] = user_agent
        websocket['client_name'] = client_name
        websocket['user_id'] = user_id
        websocket['players'] = {}

        connection_id = str(uuid.uuid4())
        websocket['connection_id'] = connection_id
        self.connections[connection_id] = websocket

        logger.info(f'Websocket connection from <{client_name}> established.')

        # Handle incoming messages
        async for message in websocket:  # type: aiohttp.WSMessage

            try:
                payload = message.json()
                logger.debug(f'Received payload from <{client_name}>.\nPayload: {payload}')
            except Exception:
                logger.error(f'Received payload with invalid JSON format from <{client_name}>.\nPayload: {message.data}')
                continue

            op = payload.get('op')
            data = payload.get('d')

            if not op or not data:
                logger.error(f'Received payload with missing "op" and/or "data" keys from <{client_name}>. Discarding.')
                continue

            if not (guild_id := data.get('guild_id', None)):
                logger.error(f'Received payload with missing "guild_id" data key from <{client_name}>. Discarding.')
                continue

            players: dict[int, Player] = websocket['players']

            if not (player := players.get(guild_id)):
                player = Player(guild_id, user_id, self)
                websocket['players'][guild_id] = player

            await player._handle_payload(op, data)

        return websocket

    # Rest handlers

    async def search_tracks(self, request: aiohttp.web.Request) -> aiohttp.web.Response:
        search = request.query.get('query')

        data = await self.search.search_youtube(search, server=self)
        return aiohttp.web.json_response(data=data, status=200)

    async def debug_stats(self, request: aiohttp.web.Request) -> aiohttp.web.Response:
        raise NotImplementedError
