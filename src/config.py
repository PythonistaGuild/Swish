import logging

import toml

logger = logging.getLogger('swish')


try:
    CONFIG = toml.load('swish.toml')
    logger.info('Successfully loaded swish.toml configuration.')
except Exception as e:
    logger.error(f'Exception: {e} when reading swish.toml. Default config values will be used instead.')

    CONFIG = {
        'SERVER': {'host': 'localhost', 'port': 3555}
    }

    with open('swish.toml', 'w') as fp:
        toml.dump(CONFIG, fp)

    logger.info('Created default swish.toml, as an error occurred loading one.')