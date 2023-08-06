#!/usr/bin/env python
# setup
# Setup script for installing stape
#
# Copyright (C) 2018 PingThings
# For license information, see LICENSE.txt
#
# ID: setup.py [] benjamin@bengfort.com $

"""
Setup script for installing stape.
See http://bbengfort.github.io/programmer/2016/01/20/packaging-with-pypi.html
"""

##########################################################################
## Imports
##########################################################################

import os
import codecs

from setuptools import setup
from setuptools import find_packages

##########################################################################
## Package Information
##########################################################################

## Basic information
NAME         = "stape"
DESCRIPTION  = "streaming telemetry analytics for power engineers"
AUTHOR       = "PingThings"
EMAIL        = "info@pingthings.io"
LICENSE      = "Apache 2"
REPOSITORY   = "https://bitbucket.org/pingthings/stape"
PACKAGE      = "stape"

## Define the keywords
KEYWORDS     = ('power engineering', 'telemetry', 'analytics', 'time series', 'data science')

## Define the classifiers
## See https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS  = (
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Apache Software License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Scientific/Engineering :: Physics',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Utilities',
)

## Important Paths
PROJECT      = os.path.abspath(os.path.dirname(__file__))
REQUIRE_PATH = "requirements.txt"
VERSION_PATH = os.path.join(PACKAGE, "version.py")
PKG_DESCRIBE = "DESCRIPTION.rst"

## Directories to ignore in find_packages
EXCLUDES     = (
    "tests", "bin", "docs", "fixtures", "register", "notebooks", "examples",
)

##########################################################################
## Helper Functions
##########################################################################

def read(*parts):
    """
    Assume UTF-8 encoding and return the contents of the file located at the
    absolute path from the REPOSITORY joined with *parts.
    """
    with codecs.open(os.path.join(PROJECT, *parts), 'rb', 'utf-8') as f:
        return f.read()


def get_version(path=VERSION_PATH):
    """
    Reads the __init__.py defined in the VERSION_PATH to find the get_version
    function, and executes it to ensure that it is loaded correctly.
    """
    namespace = {}
    exec(read(path), namespace)
    return namespace['get_version'](short=True)


def get_requires(path=REQUIRE_PATH):
    """
    Yields a generator of requirements as defined by the REQUIRE_PATH which
    should point to a requirements.txt output by `pip freeze`.
    """
    for line in read(path).splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            yield line


##########################################################################
## Define the configuration
##########################################################################

config = {
    "name": NAME,
    "version": get_version(),
    "description": DESCRIPTION,
    "long_description": read(PKG_DESCRIBE),
    "license": LICENSE,
    "author": AUTHOR,
    "author_email": EMAIL,
    "url": REPOSITORY,
    "download_url": "{}/tarball/v{}".format(REPOSITORY, get_version()),
    "packages": find_packages(where=PROJECT, exclude=EXCLUDES),
    "install_requires": list(get_requires()),
    "classifiers": CLASSIFIERS,
    "keywords": KEYWORDS,
    "zip_safe": False,
    "scripts": [],
    "setup_requires":["pytest-runner"],
    "tests_require":["pytest"],
}


##########################################################################
## Run setup script
##########################################################################

if __name__ == '__main__':
    setup(**config)
