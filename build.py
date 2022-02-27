import platform

import PyInstaller.__main__


delim = ';' if platform.system() == 'Windows' else ':'


# Install with ffmpeg binaries...
PyInstaller.__main__.run([
    'launcher.py',
    '--name',
    'swish',
    '--distpath',
    'dist',
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
    '--onefile',
])