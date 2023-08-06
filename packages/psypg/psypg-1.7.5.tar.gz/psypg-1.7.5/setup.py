#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Open and read __version__ string where located
with open('psypg/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)

setup(
    name='psypg',
    version=version,
    description='Simple Python wrapper for Psycopg2',
    author='Gary Chambers',
    author_email='gwc@gwcmail.com',
    url='https://gitlab.com/amosmoses/psypg',
    packages=['psypg'],
    install_requires=['psycopg2-binary']
)
