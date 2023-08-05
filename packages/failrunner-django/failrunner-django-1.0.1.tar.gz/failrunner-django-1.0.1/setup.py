#!/usr/bin/env python
from os import path
from distutils.core import setup

here = path.abspath(path.dirname(__file__))

VERSION = '1.0.1'

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='failrunner-django',
    version=VERSION,
    packages=['failrunner'],
    description='A command line tool to run django tests that failed during a travis job',
    long_description=long_description,
    author='Harry White',
    url='https://github.com/harrywhite4/failrunner-django',
    entry_points={
        'console_scripts': ['failrunner=failrunner.cli:main'],
    },
    install_requires=[
        'requests'
    ],
    python_requires='>=3.5'
)
