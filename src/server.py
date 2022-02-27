from __future__ import annotations

# stdlib
import asyncio
import logging
import uuid
from collections.abc import Awaitable, Callable
from typing import Any

# packages
import aiohttp
import aiohttp.web
import aiohttp.web_response
import discord

# local
from .config import CONFIG
from .ip_rotator import IpRotator
from .player import Player
from .search import Search


logger: logging.Logger = logging.getLogger('swish.server')

JSON = dict[str, Any]
Websocket = aiohttp.web.WebSocketResponse
OpHandler = Callable[[Websocket, JSON], Awaitable[None]]


class Server(aiohttp.web.Application):

    def __init__(self):
        super().__init__()

        self.rotator = IpRotator()
        self.searcher = Search()

        self.WS_OP_HANDLERS: dict[str, OpHandler] = {
            'connect':         self.connect,
            'destroy':         self.destroy,
            'play':            self.play,
            'stop':            self.stop,
            'set_position':    self.set_position,
            'set_pause_state': self.set_pause_state,
            'set_filter':      self.set_filter,
        }

        self.add_routes(
            [
                aiohttp.web.get('/', self.websocket_handler),
                aiohttp.web.get('/search', self.search_tracks),
                aiohttp.web.get('/debug', self.debug_stats)
            ]
        )

        self.connections: dict[str, Websocket] = {}

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

    async def websocket_handler(self, request: aiohttp.web.Request) -> Websocket:

        logger.info(f'Received request to upgrade websocket from:: {request.remote}.')

        websocket = aiohttp.web.WebSocketResponse()
        await websocket.prepare(request)

        password = CONFIG['SERVER']['password']
        auth = request.headers.get('Authorization')

        if password != auth:
            logger.error(f'Authorization failed for request from:: {request.remote} with Authorization: {auth}')
            raise aiohttp.web.HTTPUnauthorized

        client_token = request.headers.get('Client-Token')
        if not client_token:
            logger.error('Unable to complete websocket handshake as your Client-Token header is missing.')
            raise aiohttp.web.HTTPBadRequest

        if not request.headers.get('User-Agent'):
            logger.warning('No User-Agent header provided. Please provide a User-Agent in future connections.')

        connection_id = str(uuid.uuid4())

        await asyncio.sleep(5)

        try:
            logger.info('Logging into discord with provided token...')

            client = discord.Client()
            await client.login(client_token)

            asyncio.create_task(client.connect())
        except discord.DiscordException:
            logger.error('Unable to complete websocket handshake, improper or invalid Client-Token passed.')
            raise aiohttp.web.HTTPUnauthorized

        websocket['client'] = client
        websocket['Connection-ID'] = connection_id
        self.connections[connection_id] = websocket

        await client.wait_until_ready()
        logger.info(f'Successful websocket handshake completed from:: {request.remote}.')

        async for message in websocket:  # type: aiohttp.WSMessage

            try:
                data = message.json()
            except Exception:
                logger.error(f'Unable to parse JSON from:: {request.remote}.')
                continue

            op = data.get('op', None)
            if not (handler := self.WS_OP_HANDLERS.get(op)):
                logger.error(f'No handler registered for op:: {op}.')
                continue

            await handler(websocket, data['d'])

        return websocket

    # Websocket handlers

    async def connect(self, ws: Websocket, data: JSON) -> None:

        try:
            guild_id = int(data['guild_id'])
            channel_id = int(data['channel_id'])
        except ValueError:
            logger.error('Invalid ID passed for connect.')
            return

        player = Player(guild_id, server=self, client=ws['client'])

        await player.connect(channel_id)

        try:
            ws["players"][guild_id] = player
        except KeyError:
            ws['players'] = {guild_id: player}

    async def destroy(self, ws: Websocket, data: JSON) -> None:

        guild_id = data['guild_id']

        if not (player := ws['players'].get(guild_id)):  # type: Player
            return

        await player.destroy()
        del ws['players'][guild_id]

    async def play(self, ws: Websocket, data: JSON) -> None:

        try:
            guild_id = int(data['guild_id'])
        except ValueError:
            logger.error('Invalid guild_id passed for play.')

        player: Player | None = ws['players'][guild_id]
        if not player:
            return

        await player.play(
            data['track_id'],
            start_position=data.get('start_position', None),
            end_position=data.get('end_position', None),
            replace=data.get('replace', None)
        )

    async def stop(self, ws: Websocket, data: JSON) -> None:
        print('Received "stop" op')

    async def set_position(self, ws: Websocket, data: JSON) -> None:
        print('Received "set_position" op')

    async def set_pause_state(self, ws: Websocket, data: JSON) -> None:
        print('Received "set_pause_state" op')

    async def set_filter(self, ws: Websocket, data: JSON) -> None:
        print('Received "set_filter" op')

    # Rest handlers

    async def search_tracks(self, request: aiohttp.web.Request) -> aiohttp.web.Response:
        search = request.query.get('query')

        data = await self.searcher.search_youtube(search, server=self)
        return aiohttp.web_response.json_response(data=data, status=200)

    async def debug_stats(self, request: aiohttp.web.Request) -> aiohttp.web.Response:
        raise NotImplementedError
