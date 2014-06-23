#!/usr/bin/env python

import os
import sys
from distutils.command.build_py import build_py
import logging

from urlo.domain import get_domain

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def _configure_tld_logger():
    logger = logging.getLogger('tldextract')

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)


class TldFileGenerator(build_py):

    def run(self):
        _configure_tld_logger()
        get_domain('http://google.com')
        build_py.run(self)


settings = dict()

# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Topic :: Internet',
    'Topic :: Utilities',
]

settings.update(
    name='urlo',
    version='0.1',
    description='Url parsing and building',
    long_description=open('README.rst').read(),
    author='Stefano Dipierro',
    license='Apache 2.0',
    url='https://github.com/dipstef/urlo',
    classifiers=CLASSIFIERS,
    keywords='unicode encoding conversion normalization charset',
    packages=['urlo'],
    test_suite='tests',
    cmdclass={'build_py': TldFileGenerator},
    package_data={'': ['hosts.txt']},
    requires=['tldextract', 'unicoder']
)

setup(**settings)