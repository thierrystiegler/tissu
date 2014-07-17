#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Project   : Tissu - Functions to handle settings with Fabric
# -----------------------------------------------------------------------------
# License   : BSD License
# -----------------------------------------------------------------------------
# Authors   : Thierry Stiegler <thierry.stiegler@gmail.com>
# -----------------------------------------------------------------------------
# See: <http://docs.python.org/distutils/introduction.html>


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from tissu.constants import VERSION

setup(
    name             = "tissu",
    version          = VERSION,
    description      = "Tissu - Functions to handle settings with Fabric",
    long_description = open('README.md').read(),
    author           = "Thierry Stiegler",
    author_email     = "thierry.stiegler@gmail.com",
    url              = "http://github.com/thierrystiegler/tissu",
    download_url     = "https://github.com/thierrystiegler/tissu/tarball/%s" % (VERSION),
    #include_package_data    = True,
    keywords         = ["fabric", "settings"],
    install_requires = ["Fabric",],
    packages         = find_packages(),
    license          = "License :: OSI Approved :: BSD License",
    classifiers      = [
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Utilities"
    ],
)
# EOF - vim: ts=4 sw=4 noet