from re import search
from pathlib import Path

from setuptools import setup

with open('myconfig/__init__.py', encoding='utf-8') as f:
    version = search(r"__version__ = '(.*?)'", f.read()).group(1)

BASE_DIR = Path(__file__).parent
README = BASE_DIR.joinpath('README.md').read_text(encoding='utf-8')

setup(
    name='myconfig',
    version=version,
    description='Python Projects Configuration Manager',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/azureswastika/myconfig',
    author='Deni',
    license='MIT',
    packages=['myconfig'],
)
