#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Project   : Tissu - Functions to handle settings with Fabric
# -----------------------------------------------------------------------------
# License   : BSD License
# -----------------------------------------------------------------------------
# Authors   : Thierry Stiegler <thierry.stiegler@gmail.com>
# -----------------------------------------------------------------------------

import os

import constants as C

from fabric.api import env, run, local
from fabric.context_managers import settings
from fabric.colors import red, green, magenta, yellow
from fabric.utils import abort, puts, warn


__all__ = [
    'current_hostdef',
    'env_attr_key_update',
    'env_attr_update',
    'get_hostdef',
    'get_current_tissu',
    'host_string',
    'hoststring_from_hostdef',
    'is_tissu_loaded',
    'load_settings',
    'set_settings_module', 
    'set_roledefs',
    'set_parallel_execution',
    'set_current_tissu'
]

os.environ[C.TISSU_SETTINGS_MODULE] = C.DEFAULT_TISSU_SETTINGS_MODULE


def set_settings_module(envname):
    """
    Load the settings module for a specific environement name
    """
    filename = "%s.py" % envname
    if os.path.exists(os.path.join(".", "settings", filename)):
        os.environ[C.TISSU_SETTINGS_MODULE] = "settings.%s" % envname
        return True
    else:
        return False

def set_roledefs():
    """
    Load the cluster nodes roles in the fabric env
    """
    from tissu.conf import settings
    roledefs = getattr(settings, C.ROLES, None)
    
    if roledefs is None or roledefs == {}:
        return False

    hosts = []
    for role in roledefs.keys():            
        hosts = hosts + roledefs[role]  
    
    roledefs['all'] = list(set(hosts))
    env.roledefs.update( roledefs )
    return True


def get_hostdef(host_string):
    return env.hostdefs.get(host_string, {})


def current_hostdef():
    return get_hostdef(env.host_string)


def set_parallel_execution():
    from tissu.conf import settings
    env.parallel = settings.FABRIC_PARALLEL_EXECUTION
    env.pool_size = settings.FABRIC_PARALLEL_POOLSIZE


def host_string(username, hostname, port=C.DEFAULT_SSH_PORT):
    return "%s@%s:%s" % (username, hostname, port)

def hoststring_from_hostdef(h):
    return host_string(h.get(C.USER), h.get(C.HOSTNAME), h.get(C.SSH_PORT, C.DEFAULT_SSH_PORT))

def set_current_tissu(envname):
    setattr(env, C.CURRENT_TISSU, envname)

def get_current_tissu():
    return getattr(env, C.CURRENT_TISSU, None)

def is_tissu_loaded():
    return get_current_tissu() is not None

def env_attr_key_update(attr, key, value):
    item = getattr(env, attr)
    item[key] = value
    setattr(env, attr, item)

def env_attr_update(attr, value):
    item = getattr(env, attr)
    item.update(value)
    setattr(env, attr, item)

def load_settings(envname=None):
    """
    Load fabric env from python settings files
    """

    set_current_tissu(None)

    if set_settings_module(envname) is False:
         msg="Unable to find  %s settings" % envname
         raise ValueError(msg)
         return False

    from tissu.conf import settings

    env.use_ssh_config = False
    if settings.FABRIC_USE_SSH_CONFIG:
        if env.ssh_config_path and os.path.isfile(os.path.expanduser(env.ssh_config_path)):
            env.use_ssh_config = True

    roledefs = getattr(settings, C.ROLES, {})
    
    all_hosts = []
    setattr(env, C.HOSTDEFS, {})

    for role,hosts in roledefs.items():
        role_hosts = [ hoststring_from_hostdef(h) for h in hosts]
        all_hosts += role_hosts
        env_attr_key_update(C.ROLEDEFS, role, role_hosts)

        passwords = {}
        for h in hosts:
            password = h.get(C.PASSWORD)
            if password is not None:
                key = hoststring_from_hostdef(h)
                passwords[key] = password

        env_attr_update(C.PASSWORDS, passwords)
            
        hostdefs = dict((hoststring_from_hostdef(h), h) for h in hosts)
        env_attr_update(C.HOSTDEFS, hostdefs)
        
        keys = [ h.get(C.HOSTKEY) for h in hosts]

        for key in keys:
            if key is not None:
                if env.key_filename is None:
                    env.key_filename = [key,]
                elif key not in env.key_filename:
                    env.key_filename.append( key )

    
 
    if len(getattr(env, C.ROLEDEFS)) == 0:
         raise KeyError("Unable to load roles is %sdefined in your settings file ?" % C.ROLES )
         return False
    else:
        env_attr_key_update(C.ROLEDEFS, C.ALL_ROLE, list(set( all_hosts )) )
        set_parallel_execution()
        setattr(env, C.MY_SETTINGS, settings)
        set_current_tissu(envname)
        return True



# EOF - vim: ts=4 sw=4 noet