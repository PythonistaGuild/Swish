from __future__ import annotations

# stdlib
import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

# packages
import aiohttp
import aiohttp.web
from discord.backoff import ExponentialBackoff
from discord.ext.native_voice import _native_voice


if TYPE_CHECKING:
    # local
    from .app import App


logger: logging.Logger = logging.getLogger('swish.player')


class Player:

    def __init__(
        self,
        app: App,
        websocket: aiohttp.web.WebSocketResponse,
        guild_id: str,
        user_id: str
    ) -> None:

        self._server: App = app
        self._websocket: aiohttp.web.WebSocketResponse = websocket
        self._guild_id: str = guild_id
        self._user_id: str = user_id

        self._connector: _native_voice.VoiceConnector = _native_voice.VoiceConnector()
        self._connection: _native_voice.VoiceConnection | None = None
        self._runner: asyncio.Task[None] | None = None

        self._connector.user_id = int(user_id)

        self.OP_HANDLERS: dict[str, Callable[[dict[str, Any]], Awaitable[None]]] = {
            'voice_update': self._voice_update,
            'destroy': self._destroy,
            'play': self._play,
            'stop': self._stop,
            'set_pause_state': self._set_pause_state,
            'set_position': self._set_position,
            'set_filter': self._set_filter,
        }

    # websocket op handlers

    async def handle_payload(self, payload: dict[str, Any]) -> None:

        handler = self.OP_HANDLERS.get(payload['op'])
        if not handler:
            logger.error(f'Received payload with unknown "op" key from <{self._websocket["client_name"]}>. Discarding.')
            return

        await handler(payload['d'])

    async def _voice_update(self, data: dict[str, Any]) -> None:

        self._connector.session_id = data['session_id']
        token = data['token']
        guild_id = data['guild_id']

        if (endpoint := data.get('endpoint')) is None:
            return

        endpoint, _, _ = endpoint.rpartition(':')
        endpoint = endpoint.removeprefix('wss://')

        self._connector.update_socket(token, guild_id, endpoint)
        await self._connect()

    async def _destroy(self, data: dict[str, Any]) -> None:
        raise NotImplementedError

    async def _play(self, data: dict[str, Any]) -> None:

        decoded = self._server.search.decode_track(data['track_id'])
        track = await self._server.search.search_youtube(decoded['id'], raw=True)
        track = track[0]

        if self._connection:
            self._connection.play(track['url'])

    async def _stop(self, data: dict[str, Any]) -> None:
        raise NotImplementedError

    async def _set_pause_state(self, data: dict[str, Any]) -> None:
        raise NotImplementedError

    async def _set_position(self, data: dict[str, Any]) -> None:
        raise NotImplementedError

    async def _set_filter(self, data: dict[str, Any]) -> None:
        raise NotImplementedError

    # internal connection handlers

    async def _connect(self) -> None:

        loop = asyncio.get_running_loop()
        self._connection = await self._connector.connect(loop)

        if self._runner is not None:
            self._runner.cancel()

        self._runner = loop.create_task(self._reconnect_handler())

    async def _reconnect_handler(self) -> None:

        loop = asyncio.get_running_loop()
        backoff = ExponentialBackoff()

        while True:

            try:
                await self._connection.run(loop)

            except _native_voice.ConnectionClosed:
                await self._disconnect()
                return

            except _native_voice.ConnectionError:
                await self._disconnect()
                return

            except _native_voice.ReconnectError:

                retry = backoff.delay()
                await asyncio.sleep(retry)

                try:
                    await self._connect()
                except asyncio.TimeoutError:
                    continue

            else:
                await self._disconnect()
                return

    async def _disconnect(self) -> None:

        if self._connection is None:
            return

        self._connection.disconnect()
        self._connection = None

        del self._websocket['players'][self._guild_id]

    # utility

    def is_playing(self) -> bool:
        return self._connection.is_playing() if self._connection else False

    def is_paused(self) -> bool:  # TODO: implement rust stuff for this
        return self._connection.is_paused() if self._connection else False

    def _debug_info(self) -> dict[str, Any]:
        return self._connection.get_state() if self._connection else {}
