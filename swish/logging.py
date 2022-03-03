"""Swish. A standalone audio player and server for bots on Discord.

Copyright (C) 2022  PythonistaGuild <https://github.com/PythonistaGuild>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import annotations

import logging
import logging.handlers
import os

import colorama

from .config import CONFIG


class ColourFormatter(logging.Formatter):

    def __init__(self, enabled: bool) -> None:

        self.enabled: bool = enabled

        if self.enabled:
            fmt = f'{colorama.Fore.CYAN}[%(asctime)s] {colorama.Style.RESET_ALL}' \
                  f'{colorama.Fore.LIGHTCYAN_EX}[%(name) 16s] {colorama.Style.RESET_ALL}' \
                  f'%(colour)s[%(levelname) 8s] {colorama.Style.RESET_ALL}' \
                  f'%(message)s'
        else:
            fmt = '[%(asctime)s] [%(name) 16s] [%(levelname) 8s] %(message)s'

        super().__init__(
            fmt=fmt,
            datefmt='%I:%M:%S %Y/%m/%d'
        )

        self.COLOURS: dict[int, str] = {
            logging.DEBUG:   colorama.Fore.MAGENTA,
            logging.INFO:    colorama.Fore.GREEN,
            logging.WARNING: colorama.Fore.YELLOW,
            logging.ERROR:   colorama.Fore.RED,
        }

    def format(self, record: logging.LogRecord) -> str:
        record.colour = self.COLOURS[record.levelno]  # type: ignore
        return super().format(record)


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
        file_handler.setFormatter(ColourFormatter(enabled=False))
        logger.addHandler(file_handler)

        # stdout handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(ColourFormatter(enabled=True))
        logger.addHandler(stream_handler)
