#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Project   : Tissu - Functions to handle settings with Fabric
# -----------------------------------------------------------------------------
# License   : BSD License
# -----------------------------------------------------------------------------
# Authors   : Thierry Stiegler <thierry.stiegler@gmail.com>
# -----------------------------------------------------------------------------

import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from tissu import VERSION
from tissu.tasks import *
from fabric.api import *


def hello():
    run("echo hello && uptime")

@roles("db")
@task
def hello_db():
    hello()

@roles("web")
@task
def hello_web():
    hello()

@roles("all")
@task
def hello_all():
    hello()

@task
def release_github():
    local('git commit -a -m "Release %s"' % VERSION) 
    local('git tag %s ; true' % VERSION)
    local('git push --all ; true')

@task
def release_pypi():
    local('python setup.py clean sdist register upload')

@task
def release_doc():
    #local('sphinx-build -b html docs api')
    raise NotImplementedError()


@task
def release_clean():
    local("find . -name \"*.pyc\" -exec rm -f '{}' ';'")
    local('rm -rf api/')
    local('rm -rf build')
    local('rm -rf dist')

@task
def release_check():
    local("pylint tissu")


# EOF - vim: ts=4 sw=4 noet
