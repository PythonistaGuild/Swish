from __future__ import annotations

import platform
from pip._internal.commands import create_command

create_command("install").main(["-r", "native/requirements-dev.txt"])
create_command("install").main(["-r", "requirements-dev.txt"])
create_command("install").main(["-r", "requirements.txt"])

import PyInstaller.__main__

delim = ';' if platform.system() == 'Windows' else ':'


# Install with ffmpeg binary
PyInstaller.__main__.run([
    'launcher.py',
    '--name',
    'swish',
    '--distpath',
    'dist',
    '--exclude-module',
    '_bootlocale',
    '--onefile',
    '--add-binary',
    f'./bin/ffmpeg.exe{delim}.'
])
