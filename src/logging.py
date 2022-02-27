from __future__ import annotations

# stdlib
import logging
import logging.handlers
import os

# local
from src.config import CONFIG


RESET: str = '\u001b[0m'
BOLD: str = '\u001b[1m'
REVERSE: str = '\u001b[7m'
GREEN: str = '\u001b[32m'
YELLOW: str = '\u001b[33m'
MAGENTA: str = '\u001b[35m'
CYAN: str = '\u001b[36m'

loggers: dict[str, logging.Logger] = {}


def setup() -> None:

    loggers['swish'] = logging.getLogger('swish')
    loggers['discord'] = logging.getLogger('discord')
    loggers['aiohttp'] = logging.getLogger('aiohttp')

    loggers['swish'].setLevel(CONFIG['LOGGING']['LEVEL']['swish'])
    loggers['discord'].setLevel(CONFIG['LOGGING']['LEVEL']['discord'])
    loggers['aiohttp'].setLevel(CONFIG['LOGGING']['LEVEL']['aiohttp'])

    for name, logger in loggers.items():

        path = CONFIG["LOGGING"]["path"]

        if not os.path.exists(path):
            os.makedirs(path)

        # file handler
        file_handler = logging.handlers.RotatingFileHandler(
            filename=f'{path}{name}.log',
            mode='w',
            maxBytes=CONFIG['LOGGING']['max_bytes'],
            backupCount=CONFIG['LOGGING']['backup_count'],
            encoding='utf-8',
        )
        file_handler.setFormatter(
            logging.Formatter(
                fmt='%(asctime)s '
                    '[%(name) 30s] '
                    '[%(filename) 20s] '
                    '[%(levelname) 7s] '
                    '%(message)s',
                datefmt='%I:%M:%S %p %d/%m/%Y'
            )
        )
        logger.addHandler(file_handler)

        # stdout handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(
            logging.Formatter(
                fmt=f'{CYAN}%(asctime)s{RESET} '
                    f'{YELLOW}[%(name) 30s]{RESET} '
                    f'{GREEN}[%(filename) 20s]{RESET} '
                    f'{BOLD}{REVERSE}{MAGENTA}[%(levelname) 7s]{RESET} '
                    f'%(message)s',
                datefmt='%I:%M:%S %p %d/%m/%Y',
            )
        )
        logger.addHandler(stream_handler)
