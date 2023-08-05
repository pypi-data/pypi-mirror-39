#!/usr/bin/env python
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

VERSION = '1.0.4'

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='failrunner-django',
    version=VERSION,
    license='MIT',
    packages=['failrunner'],
    description='A command line tool to run django tests that failed during a travis job',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Harry White',
    author_email='harry.white424@gmail.com',
    url='https://github.com/harrywhite4/failrunner-django',
    entry_points={
        'console_scripts': ['failrunner=failrunner.cli:main'],
    },
    install_requires=[
        'requests'
    ],
    python_requires='>=3.5',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
