#!/usr/bin/python3
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


# README
with open('README.md', 'r') as file:
    long_desc = file.read()


# version string
__version__ = '0.4.0.post2'


# set-up script for pip distribution
setup(
    name = 'jspcapy',
    version = __version__,
    author = 'Jarry Shaw',
    author_email = 'jarryshaw@icloud.com',
    url = 'https://github.com/JarryShaw/jspcapy',
    license = 'GNU General Public License v3 (GPLv3)',
    keywords = 'computer-networking pcap-analyzer pcap-parser',
    description = 'A command line pcap file analyser tool.',
    long_description = long_desc,
    long_description_content_type='text/markdown',
    python_requires = '>=3.6',
    include_package_data=True,
    zip_safe=True,
    install_requires = ['jspcap'],
    py_modules = ['jspcapy'],
    entry_points = {
        'console_scripts': [
            'jspcapy = jspcapy:main',
        ]
    },
    package_data = {
        '': [
            'LICENSE.txt',
            'README.md',
        ],
    },
    classifiers = [
        'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: System :: Networking',
        'Topic :: Utilities',
    ]
)
