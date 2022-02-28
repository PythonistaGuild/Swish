from __future__ import annotations

import logging
from typing import Any

import toml


logger: logging.Logger = logging.getLogger('swish.config')


try:
    CONFIG: dict[str, Any] = toml.load('swish.toml')  # type: ignore
    logger.info('Successfully loaded swish.toml configuration.')
except Exception as e:
    logger.error(f'Exception: {e} when reading swish.toml. Default config values will be used instead.')

    CONFIG: dict[str, Any] = {
        'SERVER': {'host': 'localhost', 'port': 3555, 'password': 'helloworld!'},
        'IP': {'blocks': []},
        'LOGGING': {'path': 'logs/', 'backup_count': 5, 'max_bytes': 5242880,
                    'LEVEL': {'swish': 'DEBUG', 'discord': 'NOTSET', 'aiohttp': 'NOTSET'}}

    }

    with open('swish.toml', 'w') as fp:
        toml.dump(CONFIG, fp)

    logger.info('Created default swish.toml, as an error occurred loading one.')
