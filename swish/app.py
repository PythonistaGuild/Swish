"""Swish. A standalone audio player and server for bots on Discord.

Copyright (C) 2022 PythonistaGuild <https://github.com/PythonistaGuild>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import annotations

import base64
import contextlib
import functools
import json
import logging
import os
from typing import Any

import aiohttp
import aiohttp.web
import yarl
import yt_dlp

from .config import CONFIG
from .player import Player
from .rotator import BanRotator, NanosecondRotator
from .types.payloads import ReceivedPayload


__all__ = (
    'App',
)


LOG: logging.Logger = logging.getLogger('swish.app')


class App(aiohttp.web.Application):

    def __init__(self) -> None:
        super().__init__()

        self._connections: list[aiohttp.web.WebSocketResponse] = []

        self.add_routes(
            [
                aiohttp.web.get('/', self.websocket_handler),
                aiohttp.web.get('/search', self.search_tracks),
            ]
        )

    async def run(self) -> None:

        runner = aiohttp.web.AppRunner(
            app=self
        )
        await runner.setup()

        host = CONFIG.server.host
        port = CONFIG.server.port

        site = aiohttp.web.TCPSite(
            runner=runner,
            host=host,
            port=port
        )
        await site.start()

        LOG.info(f'Swish server started on {host}:{port}')

    # websocket handling

    async def websocket_handler(self, request: aiohttp.web.Request) -> aiohttp.web.WebSocketResponse:

        LOG.info(f'<{request.remote}> - Incoming websocket connection request.')

        websocket = aiohttp.web.WebSocketResponse()
        await websocket.prepare(request)

        user_agent: str | None = request.headers.get('User-Agent')
        if not user_agent:
            LOG.error(f'<{request.remote}> - Websocket connection failed due to missing \'User-Agent\' header.')
            await websocket.close(code=4000, message=b'Missing \'User-Agent\' header.')
            return websocket

        client_name = f'<{user_agent} ({request.remote})>'

        user_id: str | None = request.headers.get('User-Id')
        if not user_id:
            LOG.error(f'{client_name} - Websocket connection failed due to missing \'User-Id\' header.')
            await websocket.close(code=4000, message=b'Missing \'User-Id\' header.')
            return websocket

        password: str = CONFIG.server.password
        authorization: str | None = request.headers.get('Authorization')
        if password != authorization:
            LOG.error(f'{client_name} - Websocket connection failed due to mismatched \'Authorization\' header.')
            await websocket.close(code=4001, message=b'Authorization failed.')
            return websocket

        websocket['client_name'] = client_name
        websocket['user_agent'] = user_agent
        websocket['user_id'] = user_id
        websocket['app'] = self
        websocket['players'] = {}
        self._connections.append(websocket)

        LOG.info(f'{client_name} - Websocket connection established.')

        message: aiohttp.WSMessage
        async for message in websocket:

            try:
                payload: ReceivedPayload = message.json()
            except json.JSONDecodeError:
                LOG.error(f'{client_name} - Received payload with invalid JSON format.\nPayload: {message.data}')
                continue

            if 'op' not in payload:
                LOG.error(f'{client_name} - Received payload with missing \'op\' key.\nPayload: {payload}')
                continue
            if 'd' not in payload:
                LOG.error(f'{client_name} - Received payload with missing \'d\' key.\nPayload: {payload}')
                continue

            # op codes that don't require player should be handled here.
            # TODO: handle debug op

            guild_id: str | None = payload['d'].get('guild_id')
            if not guild_id:
                LOG.error(f'{client_name} - Received payload with missing \'guild_id\' data key. Payload: {payload}')
                continue

            player: Player | None = websocket['players'].get(guild_id)
            if not player:
                player = Player(websocket, guild_id)
                websocket['players'][guild_id] = player

            await player.handle_payload(payload)

        LOG.info(f'{client_name} - Websocket connection closed.')

        # TODO: destroy/disconnect all players
        self._connections.remove(websocket)
        return websocket

    # search handling

    @staticmethod
    def _encode_track_info(info: dict[str, Any], /) -> str:
        return base64.b64encode(json.dumps(info).encode()).decode()

    @staticmethod
    def _decode_track_id(_id: str, /) -> dict[str, Any]:
        return json.loads(base64.b64decode(_id).decode())

    _SEARCH_OPTIONS: dict[str, Any] = {
        'quiet':              True,
        'no_warnings':        True,
        'format':             'bestaudio[ext=webm][acodec=opus]/'
                              'bestaudio[ext=mp4][acodec=aac]/'
                              'bestvideo[ext=mp4][acodec=aac]/'
                              'best',
        'restrictfilenames':  False,
        'ignoreerrors':       True,
        'logtostderr':        False,
        'noplaylist':         False,
        'nocheckcertificate': True,
        'default_search':     'auto',
        'source_address':     '0.0.0.0',
    }

    _SOURCE_MAPPING: dict[str, str] = {
        'youtube':    f'ytsearch{CONFIG.search.max_results}:',
        'soundcloud': f'scsearch{CONFIG.search.max_results}:',
        'niconico':   f'nicosearch{CONFIG.search.max_results}:',
        'bilibili':   f'bilisearch{CONFIG.search.max_results}:',
        'none':       ''
    }

    _ROTATOR_MAPPING: dict[str, type[NanosecondRotator] | type[BanRotator]] = {
        'nanosecond-rotator': NanosecondRotator,
        'ban-rotator':        BanRotator
    }

    async def _ytdl_search(self, query: str, internal: bool) -> Any:

        self._SEARCH_OPTIONS['extract_flat'] = not internal
        if CONFIG.rotation.enabled:
            self._SEARCH_OPTIONS['source_address'] = self._ROTATOR_MAPPING[CONFIG.rotation.method].rotate()

        with yt_dlp.YoutubeDL(self._SEARCH_OPTIONS) as YTDL:
            with contextlib.redirect_stdout(open(os.devnull, 'w')):
                assert self._loop is not None
                _search: Any = await self._loop.run_in_executor(
                    None,
                    functools.partial(YTDL.extract_info, query, download=False)
                )

        return YTDL.sanitize_info(_search)  # type: ignore

    async def _get_playback_url(self, url: str) -> str:

        search = await self._ytdl_search(url, internal=True)
        return search['url']

    async def _get_tracks(self, query: str) -> list[dict[str, Any]]:

        search = await self._ytdl_search(query, internal=False)

        entries = search.get('entries', [search])
        tracks: list[dict[str, Any]] = []

        for entry in entries:
            info: dict[str, Any] = {
                'title':      entry['title'],
                'identifier': entry['id'],
                'url':        entry['url'],
                'length':     int(entry.get('duration') or 0 * 1000),
                'author':     entry.get('uploader', 'Unknown'),
                'author_id':  entry.get('channel_id', None),
                'thumbnail':  entry.get('thumbnails', [None])[0],
                'is_live':    entry.get('live_status', False),
            }
            tracks.append(
                {
                    'id':   self._encode_track_info(info),
                    'info': info
                }
            )

        return tracks

    async def search_tracks(self, request: aiohttp.web.Request) -> aiohttp.web.Response:

        query = request.query.get('query')
        if not query:
            return aiohttp.web.json_response({'error': 'Missing \'query\' query parameter.'}, status=400)

        source = request.query.get('source', 'youtube')
        if (url := yarl.URL(query)) and url.host and url.scheme:
            source = 'none'

        prefix = self._SOURCE_MAPPING.get(source)
        if prefix is None:
            return aiohttp.web.json_response({'error': 'Invalid \'source\' query parameter.'}, status=400)

        tracks = await self._get_tracks(f'{prefix}{query}')

        return aiohttp.web.json_response(tracks)
