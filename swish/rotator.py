"""Swish. A standalone audio player and server for bots on Discord.

Copyright (C) 2022  PythonistaGuild <https://github.com/PythonistaGuild>

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
import logging
import random

from .config import CONFIG


logger: logging.Logger = logging.getLogger('swish.rotator')


Network = ipaddress.IPv4Network | ipaddress.IPv6Network
IP = ipaddress.IPv4Address | ipaddress.IPv6Address


class IpRotator:

    _blocks = CONFIG['IP']['blocks']
    _networks: list[Network] = [ipaddress.ip_network(ip) for ip in _blocks]

    if _networks:
        _total: int = sum(network.num_addresses for network in _networks)
        logger.info(f'IP rotation enabled using {_total} total addresses.')
    else:
        _total: int = 0
        logger.warning('No IP blocks configured. Increased risk of rate-limiting.')

    _banned: list[IP] = []
    _current: IP | None = None

    @classmethod
    def rotate(cls) -> str:

        if not cls._networks:
            return '0.0.0.0'

        if cls._current:
            cls._banned.append(cls._current)
            logger.debug(f'Banned IP: {cls._current}')

        for ip in random.choice(cls._networks):

            if ip == cls._current or ip in cls._banned:
                continue

            logger.info(f'Rotated to new IP: {ip}')
            cls._current = ip
            break

        return str(cls._current)
