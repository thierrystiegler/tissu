#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Project   : Tissu - Functions to handle settings with Fabric
# -----------------------------------------------------------------------------
# License   : BSD License
# -----------------------------------------------------------------------------
# Authors   : Thierry Stiegler <thierry.stiegler@gmail.com>
# -----------------------------------------------------------------------------

import inspect, os, sys

from fabric.api import env, run, local
from fabric.decorators import task, roles
from fabric.colors import red, green, magenta, yellow
from fabric.utils import abort, puts, warn
from tissu.api import load_settings, is_tissu_loaded
from tissu import constants as C


DEFAULT_PYTHON_TPL = """# -*- coding: utf-8 -*-
# generate with tissu                
import os

PROJECT_PATH =  os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

# Sample of configuration
#
# A = { 
#  "user" : "foo",
#  "hostname" : "localhost",
#  "password": "password",
# }
# 
# B = { 
#  "user" : "bar",
#  "hostname" : "server.example.org",
#  "key": "/home/bar/.ssh/id_rsa.pub"
# 
# }
# 
# C = { 
#  "user" : "john",
#  "hostname" : "server2.example.org",
#  "port": "22000",
#  "password" : "supermario",
# }
# 
# %(roles)s = {
#     "db":       [A],
#     "web":      [B,C],
# }
# 
%(roles)s = {}
""" % {
    "roles" : C.ROLES
}


@task 
def tissu_print():
    if is_tissu_loaded():
        puts(magenta("Fabric env :"))

        keys = env.keys()
        keys.sort()
        for k in keys:
            v = env[k]
            puts("%s : %s" % ( yellow(k),v ) )

        puts("\n")
        puts(magenta("Tissu settings :"))
        from tissu.conf import settings
        public_props = (name for name in dir(settings) if not name.startswith('_'))
        for k in public_props:
            puts("%s : %s" % ( yellow(k),getattr(settings, k) ) )

    else:
        abort(red("No environnement loaded, please run fab e:{envnanme}"))


@task
def e(envname):
    """
    Environnement loader
    """
    if envname is not None:
        try:
            load_settings(envname)
            msg = green("Environment %s sucessfully loaded :)" % envname)
            puts(msg)

        except Exception, e:
            import traceback
            traceback.print_exc()
            
            msg = "\n\nERREUR: %s" % e
            puts(red(msg))       
    else:
        abort(red("Please give an environment name :( \n$ fab e:production"))


@task
def tissu_init():
    """
    Init the settings scaffolding
    """

    basedir = C.SETTINGS_DIRNAME
    if not os.path.exists(basedir):
        local("mkdir -p %s" % basedir)

    initpy = os.path.join(basedir, "__init__.py")
    if not os.path.exists(initpy):
        local("touch settings/__init__.py")

    defaultpy = os.path.join(basedir, C.DEFAULT_SETTINGS_FILENAME)
    if not os.path.exists(defaultpy):
        f = open(defaultpy, "w+")
        f.write(DEFAULT_PYTHON_TPL)
        puts("%s written" % defaultpy)

# EOF - vim: ts=4 sw=4 noet