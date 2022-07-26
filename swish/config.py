"""Swish. A standalone audio player and server for bots on Discord.

Copyright (C) 2022 PythonistaGuild <https://github.com/PythonistaGuild>

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

import dataclasses
import sys
from typing import Any, Literal

import dacite
import toml


__all__ = (
    'CONFIG',
)


DEFAULT_CONFIG: dict[str, Any] = {
    'server':   {
        'host':     '127.0.0.1',
        'port':     8000,
        'password': 'helloworld!'
    },
    'rotation': {
        'enabled': False,
        'method':  'nanosecond-rotator',
        'blocks':  []
    },
    'search':   {
        'max_results': 10
    },
    'logging':  {
        'path':         'logs/',
        'backup_count': 5,
        'max_bytes':    (2 ** 20) * 5,
        'levels':       {
            'swish':   'DEBUG',
            'aiohttp': 'NOTSET'
        }
    }
}


@dataclasses.dataclass
class Server:
    host: str
    port: int
    password: str


@dataclasses.dataclass
class Rotation:
    enabled: bool
    method: Literal['nanosecond-rotator', 'ban-rotator']
    blocks: list[str]


@dataclasses.dataclass
class Search:
    max_results: int


@dataclasses.dataclass
class LoggingLevels:
    swish: Literal['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']
    aiohttp: Literal['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']


@dataclasses.dataclass
class Logging:
    path: str
    backup_count: int
    max_bytes: int
    levels: LoggingLevels


@dataclasses.dataclass
class Config:
    server: Server
    rotation: Rotation
    search: Search
    logging: Logging


def load_config() -> Config:

    try:
        return dacite.from_dict(Config, toml.load('swish.toml'))

    except (toml.TomlDecodeError, FileNotFoundError):

        with open('swish.toml', 'w') as fp:
            toml.dump(DEFAULT_CONFIG, fp)

        print('Could not find or parse swish.toml, using default configuration values.')
        return dacite.from_dict(Config, DEFAULT_CONFIG)

    except dacite.DaciteError as error:
        sys.exit(f'Your swish.toml configuration file is invalid: {str(error).capitalize()}.')


CONFIG: Config = load_config()
