from __future__ import annotations

import asyncio
from typing import Any

import aiohttp
import discord
import discord.types.voice
import toml
from discord.ext import commands


CONFIG: dict[str, Any] = toml.load('swish.toml')  # type: ignore


class CD(commands.Bot):

    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or('cb '),
            intents=discord.Intents.all(),
            case_insensitive=True,
        )

        self.first_ready: bool = True

        self.session: aiohttp.ClientSession | None = None
        self.websocket: aiohttp.ClientWebSocketResponse | None = None
        self.task: asyncio.Task[None] | None = None

    async def on_ready(self) -> None:

        if not self.first_ready:
            return

        self.first_ready = False

        self.session = aiohttp.ClientSession()
        self.websocket = await self.session.ws_connect(
            url=f'ws://{CONFIG["SERVER"]["host"]}:{CONFIG["SERVER"]["port"]}',
            headers={
                'Authorization': CONFIG['SERVER']['password'],
                'User-Agent':    'Python/v3.10.1,swish.py/v0.0.1a',
                'User-Id':       str(self.user.id),
            },
        )
        self.task = asyncio.create_task(self._listen())

        print('Bot is ready!')

    async def _listen(self) -> None:

        while True:
            message = await self.websocket.receive()
            payload = message.json()

            asyncio.create_task(self._receive_payload(payload['op'], data=payload['d']))

    async def _receive_payload(self, op: str, /, *, data: dict[str, Any]) -> None:
        raise NotImplementedError

    async def _send_payload(self, op: str, data: dict[str, Any]) -> None:

        await self.websocket.send_json(
            data={
                'op': op,
                'd':  data,
            }
        )


class Player(discord.VoiceProtocol):

    def __init__(self, client: CD, channel: discord.VoiceChannel) -> None:
        super().__init__(client, channel)

        self.bot: CD = client
        self.voice_channel: discord.VoiceChannel = channel

        self._voice_server_update_data: discord.types.voice.VoiceServerUpdate | None = None
        self._session_id: str | None = None

    async def on_voice_server_update(
        self,
        data: discord.types.voice.VoiceServerUpdate
    ) -> None:

        self._voice_server_update_data = data
        await self._dispatch_voice_update()

    async def on_voice_state_update(
        self,
        data: discord.types.voice.GuildVoiceState
    ) -> None:

        self._session_id = data.get('session_id')
        await self._dispatch_voice_update()

    async def _dispatch_voice_update(self) -> None:

        if not self._session_id or not self._voice_server_update_data:
            return

        await self.bot._send_payload(
            'voice_update',
            data={'session_id': self._session_id, **self._voice_server_update_data},
        )

    async def connect(
        self,
        *,
        timeout: float | None = None,
        reconnect: bool | None = None,
        self_mute: bool = False,
        self_deaf: bool = True,
    ) -> None:
        await self.voice_channel.guild.change_voice_state(
            channel=self.voice_channel,
            self_mute=self_mute,
            self_deaf=self_deaf
        )

    async def disconnect(
        self,
        *,
        force: bool = False
    ) -> None:
        await self.voice_channel.guild.change_voice_state(channel=None)
        self.cleanup()


class Music(commands.Cog):

    def __init__(self, bot: CD) -> None:
        self.bot: CD = bot

    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str) -> None:

        if not ctx.guild.me.voice:
            await ctx.author.voice.channel.connect(cls=Player)

        async with self.bot.session.get(
                url='http://127.0.0.1:8000/search',
                params={'query': query},
        ) as response:

            data = await response.json()
            await self.bot._send_payload(
                'play',
                data={'guild_id': str(ctx.guild.id), 'track_id': data[0]['id']},
            )


cd = CD()

cd.load_extension('jishaku')
cd.add_cog(Music(cd))

cd.run('')
