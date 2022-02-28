from __future__ import annotations

import logging
import logging.handlers
import os

import colorama

from .config import CONFIG


def setup_logging() -> None:

    colorama.init(autoreset=True)

    loggers: dict[str, logging.Logger] = {
        'swish':   logging.getLogger('swish'),
        'aiohttp': logging.getLogger('aiohttp'),
    }
    loggers['swish'].setLevel(CONFIG['LOGGING']['LEVEL']['swish'])
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
