#!/usr/bin/python
# coding=utf-8

from __future__ import absolute_import, unicode_literals

from setuptools import setup
from codecs import open
from os import path
import apkverify

here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name=apkverify.__title__,
    version=apkverify.__version__,
    description=apkverify.__description__,
    long_description=readme,
    long_description_content_type='text/markdown',
    author=apkverify.__author__,
    author_email=apkverify.__author_email__,
    url=apkverify.__url__,
    license=apkverify.__license__,
    packages=['apkverify'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=['asn1crypto>=0.24.0'],
    include_package_data=False,
    platforms='any',
    keywords=['apk', 'signature', 'verify'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
