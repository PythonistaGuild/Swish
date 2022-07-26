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

import ipaddress
import itertools
import logging
import time

import discord.utils
from collections.abc import Iterator

from .config import CONFIG
from .utilities import plural


__all__ = (
    'BaseRotator',
    'NanosecondRotator',
    'BanRotator',
)


LOG: logging.Logger = logging.getLogger('swish.rotator')


Network = ipaddress.IPv4Network | ipaddress.IPv6Network


class BaseRotator:

    _enabled: bool
    _networks: list[Network]
    _address_count: int

    _cycle: Iterator[Network]
    _current_network: Network

    if CONFIG.rotation.blocks:
        _enabled = True
        _networks = [ipaddress.ip_network(block) for block in CONFIG.rotation.blocks]
        _address_count = sum(network.num_addresses for network in _networks)
        LOG.info(
            f'IP rotation enabled using {plural(_address_count, "IP")} from {plural(len(_networks), "network block")}.'
        )
        _cycle = itertools.cycle(_networks)
        _current_network = next(_cycle)

    else:
        _enabled = False
        _networks = []
        _address_count = 0
        _cycle = discord.utils.MISSING
        _current_network = discord.utils.MISSING

        LOG.warning('No network blocks configured, increased risk of ratelimiting.')

    @classmethod
    def rotate(cls) -> ...:
        raise NotImplementedError


class BanRotator(BaseRotator):

    _offset: int = 0

    @classmethod
    def rotate(cls) -> str:

        if not cls._enabled:
            return '0.0.0.0'

        if cls._offset >= cls._current_network.num_addresses:
            cls._current_network = next(cls._cycle)
            cls._offset = 0

        address = cls._current_network[cls._offset]
        cls._offset += 1

        return str(address)


class NanosecondRotator(BaseRotator):

    _ns: int = time.time_ns()

    @classmethod
    def rotate(cls) -> str:

        if not cls._enabled or cls._address_count < 2 ** 64:
            return '0.0.0.0'

        while True:

            offset = time.time_ns() - cls._ns

            if offset > cls._address_count:
                cls._ns = time.time_ns()
                continue
            elif offset >= cls._current_network.num_addresses:
                cls._current_network = next(cls._cycle)
                offset -= cls._current_network.num_addresses
            else:
                break

        return str(cls._current_network[offset])
