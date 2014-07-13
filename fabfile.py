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




# EOF - vim: ts=4 sw=4 noet