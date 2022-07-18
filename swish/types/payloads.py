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

from collections.abc import Awaitable, Callable
from typing import Any, Literal, TypedDict, Union

from typing_extensions import NotRequired


__all__ = (
    # Received
    "VoiceUpdateData",
    "PlayData",
    "SetPauseStateData",
    "SetPositionData",
    "SetFilterData",

    "ReceivedPayloadOp",
    "ReceivedPayload",

    # Sent
    "EventData",

    "SentPayloadOp",
    "SentPayload",

    # Final
    "PayloadHandlers",
    "Payload",
)


############
# Received #
############

class VoiceUpdateData(TypedDict):
    guild_id: str
    session_id: str
    token: str
    endpoint: str


class PlayData(TypedDict):
    guild_id: str
    track_id: str
    start_time: NotRequired[int]
    end_time: NotRequired[int]
    replace: NotRequired[bool]


class SetPauseStateData(TypedDict):
    guild_id: str
    state: bool


class SetPositionData(TypedDict):
    guild_id: str
    position: int


class SetFilterData(TypedDict):
    guild_id: str


ReceivedPayloadOp = Literal[
    'voice_update',
    'destroy',
    'play',
    'stop',
    'set_pause_state',
    'set_position',
    'set_filter',
]


class ReceivedPayload(TypedDict):
    op: ReceivedPayloadOp
    d: Any


########
# Sent #
########

class EventData(TypedDict):
    guild_id: str
    type: Literal['track_start', 'track_end', 'track_error', 'track_update', 'player_debug']


SentPayloadOp = Literal['event']


class SentPayload(TypedDict):
    op: SentPayloadOp
    d: Any


#########
# Final #
#########


class PayloadHandlers(TypedDict):
    voice_update: Callable[[VoiceUpdateData], Awaitable[None]]
    destroy: Callable[..., Awaitable[None]]
    play: Callable[[PlayData], Awaitable[None]]
    stop: Callable[..., Awaitable[None]]
    set_pause_state: Callable[[SetPauseStateData], Awaitable[None]]
    set_position: Callable[[SetPositionData], Awaitable[None]]
    set_filter: Callable[[SetFilterData], Awaitable[None]]


Payload = Union[ReceivedPayload, SentPayload]
