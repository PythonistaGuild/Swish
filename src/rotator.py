import ipaddress
import logging
import random

from config import CONFIG


logger = logging.getLogger('swish')


class IPRotator:

    def __init__(self):
        self._blocks = CONFIG['IP']['blocks']
        self._banned = []

        if self._blocks:
            self.networks = [ipaddress.ip_network(ip) for ip in self._blocks]

            self.total = 0
            for network in self.networks:
                self.total += network.num_addresses

            logger.info(f'Using rotating IP addresses with {self.total} total addresses...')
        else:
            logger.warning('No IP rotating has been set up. This may result in being rate-limited.')

    def get_random_ip(self) -> str:
        logger.debug('Generating new IP address from random network.')

        network = random.choice(self.networks)
        while True:
            ip = random.choice(network.hosts())

            if ip in self._banned:
                continue

            logger.info(f'Generated new IP: {ip}')
            return ip

