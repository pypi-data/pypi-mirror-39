#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from distutils.core import setup

version = '0.6.7'

setup(name='aiolifx',
    packages=['aiolifx'],
    version=version,
    author='François Wautier',
    author_email='francois@wautier.eu',
    description='API for local communication with LIFX devices over a LAN with asyncio.',
    url='http://github.com/frawau/aiolifx',
    download_url='https://github.com/frawau/aiolifx/archive/'+version+'.tar.gz',
    keywords = ['lifx', 'light', 'automation'],
    license='MIT',
    install_requires=[
    "bitstring",
    "ifaddr",
    ],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4'
    ])
