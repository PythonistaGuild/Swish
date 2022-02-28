from __future__ import annotations

# stdlib
import asyncio
from typing import Any

# packages
import aiohttp
import discord
import discord.types.voice
from discord.ext import commands

# local
from src.config import CONFIG


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix='>?')

        self.first_ready: bool = True

        self.session: aiohttp.ClientSession | None = None
        self._ws: aiohttp.ClientWebSocketResponse | None = None
        self.task: asyncio.Task[None] | None = None

    async def on_ready(self):

        if not self.first_ready:
            return

        self.first_ready = False

        self.session = aiohttp.ClientSession()

        self._ws = await self.session.ws_connect(
            url=f'ws://{CONFIG["SERVER"]["host"]}:{CONFIG["SERVER"]["port"]}',
            headers={
                'Authorization': CONFIG['SERVER']['password'],
                'User-Agent':    'Python/3.10 swish.py/v0.0.1a',
                'User-Id':       str(self.user.id),
            },
        )

        self.task = asyncio.create_task(self._listen())

        print('Bot is ready!')

    async def _listen(self) -> None:

        while True:
            message = await self._ws.receive()
            payload = message.json()

            asyncio.create_task(self._receive_payload(payload["op"], data=payload["d"]))

    async def _receive_payload(self, op: str, /, *, data: dict[str, Any]) -> None:
        raise NotImplementedError

    async def _send_payload(self, op: str, /, *, data: dict[str, Any]) -> None:

        payload = {
            "op": op,
            "d": data,
        }
        await self._ws.send_json(payload)


class Player(discord.VoiceProtocol):

    def __init__(self, client: Bot, channel: discord.VoiceChannel) -> None:
        super().__init__(client, channel)

        self._voice_server_update_data: discord.types.voice.VoiceServerUpdate | None = None
        self._session_id: str | None = None

        self.bot = client
        self.voice_channel = channel

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

        self._session_id = data.get("session_id")
        await self._dispatch_voice_update()

    async def _dispatch_voice_update(self) -> None:

        if not self._session_id or not self._voice_server_update_data:
            return

        await self.bot._send_payload(
            "voice_update",
            data={"session_id": self._session_id, **self._voice_server_update_data},
        )

    async def connect(
        self,
        *,
        timeout: float | None = None,
        reconnect: bool | None = None,
        self_mute: bool = False,
        self_deaf: bool = True,
    ) -> None:

        await self.voice_channel.guild.change_voice_state(channel=self.voice_channel, self_mute=self_mute, self_deaf=self_deaf)

    async def disconnect(
        self,
        *,
        force: bool = False
    ) -> None:

        await self.voice_channel.guild.change_voice_state(channel=None)
        self.cleanup()


class Music(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str) -> None:

        if not ctx.guild.me.voice:
            await ctx.author.voice.channel.connect(cls=Player)

        async with self.bot.session.get(f'http://{CONFIG["SERVER"]["host"]}:{CONFIG["SERVER"]["port"]}/search?query={query}') as response:
            await self.bot._send_payload("play", data={"guild_id": str(ctx.guild.id), "track_id": (await response.json())[0]})


a = Bot()
a.add_cog(Music(a))
a.run('no token for u >:)')
