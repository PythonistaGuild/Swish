from __future__ import annotations

import platform

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

# Install without ffmpeg binary
PyInstaller.__main__.run([
    'launcher.py',
    '--name',
    'swish',
    '--distpath',
    'dist_no_bin',
    '--exclude-module',
    '_bootlocale',
    '--onefile',
])
