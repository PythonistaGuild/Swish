from __future__ import annotations

# stdlib
import logging
import logging.handlers
import os

# packages
import colorama

# local
from src.config import CONFIG


colorama.init(autoreset=True)


RESET: str = '\033[0m'
BOLD: str = '\033[1m'
REVERSE: str = '\033[7m'
GREEN: str = '\033[1;32m'
YELLOW: str = '\033[1;33m'
MAGENTA: str = '\033[1;35m'
CYAN: str = '\033[1;36m'

loggers: dict[str, logging.Logger] = {}


def setup() -> None:

    loggers['swish'] = logging.getLogger('swish')
    loggers['discord'] = logging.getLogger('discord')
    loggers['aiohttp'] = logging.getLogger('aiohttp')

    loggers['swish'].setLevel(CONFIG['LOGGING']['LEVEL']['swish'])
    loggers['discord'].setLevel(CONFIG['LOGGING']['LEVEL']['discord'])
    loggers['aiohttp'].setLevel(CONFIG['LOGGING']['LEVEL']['aiohttp'])

    for name, logger in loggers.items():

        path = CONFIG['LOGGING']['path']

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
                    '[%(name) 16s] '
                    '[%(filename) 16s] '
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
                fmt=f'{colorama.Fore.CYAN}%(asctime)s{colorama.Style.RESET_ALL} '
                    f'{colorama.Fore.YELLOW}[%(name) 16s]{colorama.Style.RESET_ALL} '
                    f'{colorama.Fore.GREEN}[%(filename) 16s]{colorama.Style.RESET_ALL} '
                    f'{colorama.Back.LIGHTCYAN_EX}{colorama.Fore.BLACK}[%(levelname) 7s]{colorama.Style.RESET_ALL} '
                    f'%(message)s',
                datefmt='%I:%M:%S %p %d/%m/%Y',
            )
        )
        logger.addHandler(stream_handler)
