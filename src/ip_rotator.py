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

    def __init__(self) -> None:

        self._current: IP | None = None

        self._blocks = CONFIG['IP']['blocks']
        self._networks: list[Network] = [ipaddress.ip_network(ip) for ip in self._blocks]
        self._total: int = sum(network.num_addresses for network in self._networks)

        self._banned: list[IP] = []

        if not self._networks:
            logger.warning('No IP blocks configured. Increased risk of rate-limiting.')
        else:
            logger.info(f'IP rotation enabled using {self._total} total addresses.')
            self.rotate()

    def rotate(self) -> str:

        if not self._networks:
            return '0.0.0.0'

        if self._current:
            self._banned.append(self._current)
            logger.debug(f'Banned IP: {self._current}')

        for ip in random.choice(self._networks):

            if ip in self._banned or ip == self._current:
                continue

            logger.info(f'Rotated to new IP: {ip}')
            self._current = ip
            break

        return str(self._current)
