from __future__ import annotations

# stdlib
import asyncio
import logging
from typing import TYPE_CHECKING, Any

# packages
from discord.backoff import ExponentialBackoff
from discord.ext.native_voice import _native_voice


if TYPE_CHECKING:
    # local
    from .app import App


logger: logging.Logger = logging.getLogger('swish.player')


class Player:

    def __init__(self, guild_id: str, user_id: str, app: App) -> None:

        self._guild_id: str = guild_id
        self._server: App = app

        self._connector: _native_voice.VoiceConnector = _native_voice.VoiceConnector()
        self._connector.user_id = int(user_id)

        self._connection: _native_voice.VoiceConnection | None = None
        self._runner: asyncio.Task[None] | None = None

    async def _handle_payload(
        self,
        op: str,
        data: dict[str, Any]
    ) -> None:

        if op == "voice_update":
            await self._voice_update(data)
        elif op == 'play':
            await self._play(data)

    async def _voice_update(self, data: dict[str, Any]) -> None:

        self._connector.session_id = data['session_id']
        token = data.get('token')
        server_id = data['guild_id']
        endpoint = data.get('endpoint')

        if endpoint is None or token is None:
            return

        endpoint, _, _ = endpoint.rpartition(':')
        if endpoint.startswith('wss://'):
            endpoint = endpoint[6:]

        self._connector.update_socket(token, server_id, endpoint)
        await self.connect()

    async def _play(self, data: dict[str, Any]) -> None:

        decoded = self._server.search.decode_track(data['track_id'])
        track = await self._server.search.search_youtube(decoded['id'], raw=True)
        track = track[0]

        if self._connection:
            self._connection.play(track['url'])

    #

    async def connect(self) -> None:

        loop = asyncio.get_running_loop()
        self._connection = await self._connector.connect(loop)

        if self._runner is not None:
            self._runner.cancel()

        self._runner = loop.create_task(self.reconnect_handler())

    async def reconnect_handler(self) -> None:

        backoff = ExponentialBackoff()
        loop = asyncio.get_running_loop()

        while True:
            try:
                await self._connection.run(loop)
            except _native_voice.ConnectionClosed as e:
                print('Voice connection got a clean close %s', e)
                await self.disconnect()
                return
            except _native_voice.ConnectionError as e:
                print('Internal voice error: %s', e)
                await self.disconnect()
                return
            except _native_voice.ReconnectError:

                retry = backoff.delay()
                print('Disconnected from voice... Reconnecting in %.2fs.', retry)

                await asyncio.sleep(retry)
                try:
                    await self.connect()
                except asyncio.TimeoutError:
                    # at this point we've retried 5 times... let's continue the loop.
                    print('Could not connect to voice... Retrying...')
                    continue
            else:
                # The function above is actually a loop already
                # So if we're here then it exited normally
                await self.disconnect()
                return

    async def disconnect(self) -> None:
        if self._connection is not None:
            self._connection.disconnect()
            self._connection = None
