from __future__ import annotations

# stdlib
import asyncio
import base64
import contextlib
import functools
import json
import os

# packages
import yt_dlp


class Search:

    opts = {
        'format': 'bestaudio/best',
        'restrictfilenames': False,
        'noplaylist': False,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
    }

    def decode_track(self, track: base64) -> dict:
        bytes_ = base64.b64decode(track)
        return json.loads(bytes_.decode())

    def encode_track(self, info: dict, *, internal: bool = False) -> base64:
        data = {'id': info['id'], 'title': info['title']}
        if internal:
            data['url'] = info['url']

        jsons = json.dumps(data)
        bytes_ = jsons.encode()

        return base64.b64encode(bytes_).decode()

    async def search_youtube(self, query: str, server=None, *, raw: bool = False, internal: bool = False):
        self.opts['source_address'] = server.rotator.rotate() if server else '0.0.0.0'
        YTDL = yt_dlp.YoutubeDL(self.opts)

        loop = asyncio.get_running_loop()
        partial = functools.partial(YTDL.extract_info, query, download=False)

        with contextlib.redirect_stdout(open(os.devnull, 'w')):
            info = await loop.run_in_executor(None, partial)

        if 'entries' in info:
            if raw:
                tracks = [t for t in info['entries']]
            else:
                tracks = [self.encode_track(t, internal=internal) for t in info['entries']]
        else:
            if raw:
                tracks = [info]
            else:
                tracks = [self.encode_track(info, internal=internal)]

        return tracks
