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
from __future__ import annotations

import platform
import sys


if '--no-deps' not in sys.argv:
    from pip._internal.commands import create_command
    create_command('install').main(['.[build]'])
    create_command('install').main(['./native_voice'])


args: list[str] = [
    'launcher.py',
    '--name', f'swish-{platform.system().lower()}',
    '--distpath', 'dist',
    '--exclude-module', '_bootlocale',
    '--onefile',
]


import PyInstaller.__main__
PyInstaller.__main__.run(args)
