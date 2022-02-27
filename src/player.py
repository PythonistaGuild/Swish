from __future__ import annotations

# stdlib
import logging

import discord
from discord.ext.native_voice import VoiceClient


logger: logging.Logger = logging.getLogger('player')


class Player:

    def __init__(self, guild_id: int, *, client: discord.Client) -> None:
        self.guild_id: int = guild_id
        self.channel_id: int = None  # type: ignore

        self._client = client
        self.vc: VoiceClient

        self.current_track_id: str | None = None

    async def connect(self, channel_id: int) -> None:
        guild: discord.Guild = self._client.get_guild(self.guild_id)
        channel: discord.VoiceChannel = guild.get_channel(channel_id)

        if not channel:
            logger.warning('Unable to find provided channel to connect to. '
                           'Check the guild_id and channel_id and try again.')

            return

        logger.info(f'Attempting to join channel: {channel_id} - {channel.name}')
        self.vc = await channel.connect(cls=VoiceClient)

        self.vc.play('fire.mp3')

    async def destroy(self) -> None:
        # TODO: ext-native-voice stuff
        pass

    def play(
        self,
        track_id: str,
        /,
        *,
        start_position: int | None = None,
        end_position: int | None = None,
        replace: bool | None = None,
    ) -> None:

        self.current_track_id = track_id

    def stop(self) -> None:
        pass

    def set_position(self) -> None:
        pass

    def set_pause_state(self) -> None:
        pass

    def set_filter(self) -> None:
        pass
