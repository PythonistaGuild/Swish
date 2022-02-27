from __future__ import annotations

# stdlib
import logging
from typing import Any

# packages
import toml


logger = logging.getLogger('swish')


try:
    CONFIG: dict[str, Any] = toml.load('swish.toml')  # type: ignore
    logger.info('Successfully loaded swish.toml configuration.')
except Exception as e:
    logger.error(f'Exception: {e} when reading swish.toml. Default config values will be used instead.')

    CONFIG: dict[str, Any] = {
        'SERVER': {'host': 'localhost', 'port': 3555}
    }

    with open('swish.toml', 'w') as fp:
        toml.dump(CONFIG, fp)

    logger.info('Created default swish.toml, as an error occurred loading one.')
