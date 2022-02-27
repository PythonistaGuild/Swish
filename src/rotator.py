from __future__ import annotations

# stdlib
import ipaddress
import logging
import random

# local
from .config import CONFIG


logger: logging.Logger = logging.getLogger('swish.rotator')


class IPRotator:

    def __init__(self):
        self.current = None

        self._blocks = CONFIG['IP']['blocks']
        self._banned = []

        if self._blocks:
            self.networks = [ipaddress.ip_network(ip) for ip in self._blocks]

            self.total = 0
            for network in self.networks:
                self.total += network.num_addresses

            logger.info(f'Using rotating IP addresses with {self.total} total addresses...')
            self.get_ip()
        else:
            logger.warning('No IP rotating has been set up. This may result in increased rate-limiting.')

    def get_ip(self) -> str:
        logger.debug('Generating new IP address from random network.')

        network = random.choice(self.networks)
        for ip in network:

            if ip in self._banned:
                continue

            logger.info(f'Generated new IP: {ip}')

            self.current = ip
            return ip
