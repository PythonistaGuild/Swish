from __future__ import annotations

# stdlib
import ipaddress
import logging
import random

# local
from .config import CONFIG


logger: logging.Logger = logging.getLogger('swish.rotator')

Network = ipaddress.IPv4Network | ipaddress.IPv6Network


class IpRotator:

    def __init__(self) -> None:

        self._current: str | None = None

        self._blocks = CONFIG['IP']['blocks']
        self._networks: list[Network] = [ipaddress.ip_network(ip) for ip in self._blocks]
        self._total: int = sum(network.num_addresses for network in self._networks)

        self._banned: list[str] = []

        if not self._networks:
            logger.warning('No IP blocks configured. Increased risk of rate-limiting.')
        else:
            logger.info(f'IP rotation enabled using {self._total} total addresses.')
            self.rotate()

    def rotate(self) -> str:

        self._banned.append(self._current)
        logger.debug(f'Banned IP: {self._current}')

        network: Network = random.choice(self._networks)
        for ip in network:

            if ip in self._banned:
                continue

            logger.info(f'Rotated to new IP: {ip}')

            self._current = ip
            return str(ip)
