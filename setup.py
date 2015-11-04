#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from pocsuite import (
    __version__ as version, __author__ as author,
    __author_email__ as author_email, __license__ as license)

setup(
    name='pocsuite',
    version=version,
    description="A famework for poc definition, check and debug",
    long_description="""\
TODO""",
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='PoC',
    author=author,
    author_email=author_email,
    url='https://github.com/knownsec/Pocsuite',
    license=license,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'pocsuite = pocsuite.pocsuite_cli:main',
            'pcs-console = pocsuite.pocsuite_console:main',
            'pcs-verify = pocsuite.pocsuite_verify:main',
            'pcs-attack = pocsuite.pocsuite_attack:main',
        ],
    },
)
