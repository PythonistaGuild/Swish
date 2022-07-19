import setuptools_rust
from setuptools import setup


setup(
    name='discord-ext-native-voice',
    version='0.1.0',
    packages=[
        'discord.ext.native_voice'
    ],
    rust_extensions=[
        setuptools_rust.RustExtension('discord.ext.native_voice.native_voice')
    ],
    setup_requires=[
        'setuptools-rust',
        'wheel',
    ],
    zip_safe=False,
)
