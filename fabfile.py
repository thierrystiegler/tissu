#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Project   : Tissu - Functions to handle settings with Fabric
# -----------------------------------------------------------------------------
# License   : BSD License
# -----------------------------------------------------------------------------
# Authors   : Thierry Stiegler <thierry.stiegler@gmail.com>
# -----------------------------------------------------------------------------

import os, sys, StringIO

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import subprocess
import fabric
from fabric.api import *

from tissu import VERSION
from tissu.tasks import *


# TESTING PURPOSE TASKS
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

# RELEASE TASK 

@task
def release_github():
    """
    Tag the release
    """
    opts = {'version': VERSION}
    local('git tag -a %(version)s -m "Release of version %(version)s"' % opts)
    local('git push --tags')

@task
def release_pypi():
    """
    Release module to pypi
    """
    local('python setup.py clean sdist register upload')

@task
def release_docs():
    """
    Generate documentation
    """
    with lcd("docs"):
        local("sphinx-apidoc -e -P -f -o  source ../tissu/")
        local("make html")


@task
def release_clean():
    """
    Clean release files
    """
    local("find . -name \"*.pyc\" -exec rm -f '{}' ';'")
    local('rm -rf api/')
    local('rm -rf build/')
    local('rm -rf dist/')
    local('rm -rf pylint/*.txt')
    local('rm -rf docs/build/*')

@task
def release():
    """
    Release the code
    """
    release_clean()
    release_docs()
    release_github()
    release_pypi()


def _subexec(command):
    """
    Subprocess call for command that return non zero exit code...
    """
    lcwd = fabric.state.env.get('lcwd', None) or None #sets lcwd to None if it bools to false as well
    process  = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=lcwd)
    out, err = process.communicate()
    print "command : %s " % command
    print "out: %s" % out
    print "err: %s" % err


@task
def release_qa():
    """
    Pylint and PEP8 QA report generator
    
    We use subprocess instead local because pylint and pep8 don't return a zero exit code.
    This behaviour is incompatible with fabric...
    """
    lines = StringIO.StringIO(local('find . -name "*.py"', capture=True))
    for line in lines.readlines():
        print "PYLINT CHECK"
        print "-----------------------"
        pyfile = os.path.normpath(line).replace("\n","").replace("\r","")
       
        reportfilename = pyfile.replace("./", "").replace("/", "_").replace(".py", ".txt")
        reportpath = os.path.join("qa", "pylint", reportfilename)

        options = {"pyfile":pyfile, "reportpath": reportpath}
        command = "pylint  %(pyfile)s > %(reportpath)s" % options  
        _subexec(command)        

        print "PEP8 CHECK"
        print "-----------------------"
        reportpath = os.path.join("qa", "pep8", reportfilename)
        options['reportpath'] = reportpath
        command = "pep8 %(pyfile)s > %(reportpath)s" % options
        _subexec(command)

# EOF - vim: ts=4 sw=4 noet
