from __future__ import annotations

# stdlib
import logging


__log__: logging.Logger = logging.getLogger('player')


class Player:

    def __init__(self, guild_id: int) -> None:
        self.guild_id: int = guild_id

        self.current_track_id: str | None = None

    async def connect(self) -> None:
        # TODO: ext-native-voice stuff
        pass

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
