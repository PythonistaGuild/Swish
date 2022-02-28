from __future__ import annotations

# stdlib
import platform

# packages
import PyInstaller.__main__


delim = ';' if platform.system() == 'Windows' else ':'


# Install with ffmpeg binaries...
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

# Install without ffmpeg binaries...
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
