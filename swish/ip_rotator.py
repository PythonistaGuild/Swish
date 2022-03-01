from __future__ import annotations

# stdlib
import ipaddress
import logging
import random

# local
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
