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
