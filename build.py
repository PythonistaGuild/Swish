from __future__ import annotations

import sys
import platform

if '--no-deps' not in sys.argv:
    from pip._internal.commands import create_command
    create_command('install').main(['-r', 'native/requirements-dev.txt'])
    create_command('install').main(['-r', 'requirements-dev.txt'])
    create_command('install').main(['-r', 'requirements.txt'])

import PyInstaller.__main__


args = [arg for arg in [
    'launcher.py',
    '--name',
    f'{"swish" if platform.system() == "Windows" else "swish-linux" if platform.system() == "Linux" else "swish"}',
    '--distpath',
    'dist',
    '--exclude-module',
    '_bootlocale',
    '--onefile',
    f'{"--add-binary" if platform.system() != "Linux" else ""}',
    f'{"./bin/ffmpeg.exe;." if platform.system() == "Windows" else "" if platform.system() == "Linux" else "./bin/ffmpeg:."}'
] if arg]

# Install with ffmpeg binary
PyInstaller.__main__.run(args)
