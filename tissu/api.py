#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Project   : Tissu - Functions to handle settings with Fabric
# -----------------------------------------------------------------------------
# License   : BSD License
# -----------------------------------------------------------------------------
# Authors   : Thierry Stiegler <thierry.stiegler@gmail.com>
# -----------------------------------------------------------------------------

"""
Tissu API
"""

import os
from fabric.api import env

import tissu.constants as C


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
    from tissu.conf import settings as tissu_settings
    roledefs = getattr(tissu_settings, C.ROLES, None)

    if roledefs is None or roledefs == {}:
        return False

    hosts = []
    for role in roledefs.keys():
        hosts = hosts + roledefs[role]

    roledefs['all'] = list(set(hosts))
    env.roledefs.update(roledefs)
    return True


def get_hostdef(hoststr):
    """
    Get the host definition by it's host string (user@host:port)
    If not found it returns an empty dict
    """
    return env.hostdefs.get(hoststr, {})


def current_hostdef():
    """
    Return the current host definition used by Fabric
    """
    return get_hostdef(env.host_string)


def set_parallel_execution():
    """
    Enable parallel execution for Fabric tasks
    """
    from tissu.conf import settings as tissu_settings
    env.parallel = tissu_settings.FABRIC_PARALLEL_EXECUTION
    env.pool_size = tissu_settings.FABRIC_PARALLEL_POOLSIZE


def host_string(username, hostname, port=C.DEFAULT_SSH_PORT):
    """
    Format host string with arguments username, hostname and port to
    username@hostname:port
    """
    return "%s@%s:%s" % (username, hostname, port)


def hoststring_from_hostdef(hostdef):
    """
    Return the hostring with a host definition dictionnary
    """
    return host_string(
        hostdef.get(C.USER),
        hostdef.get(C.HOSTNAME),
        hostdef.get(C.SSH_PORT, C.DEFAULT_SSH_PORT)
    )


def set_current_tissu(envname):
    """
    Set the current tissu settings environnement name
    """
    setattr(env, C.CURRENT_TISSU, envname)


def get_current_tissu():
    """
    Get the current tissu settings environnement name
    """
    return getattr(env, C.CURRENT_TISSU, None)


def is_tissu_loaded():
    """
    Test if a tissu settings environnement is loaded
    """
    return get_current_tissu() is not None


def env_attr_key_update(attr, key, value):
    """
    Updateone key of a dict attribut of the fabric environnement
    """
    item = getattr(env, attr)
    item[key] = value
    setattr(env, attr, item)


def env_attr_update(attr, value):
    """
    Update a dict attribute of the fabric environnement
    """
    item = getattr(env, attr)
    item.update(value)
    setattr(env, attr, item)


def sshconfig_exists(sshconfig_path):
    """
    Test if the ssh config path exists
    """
    return os.path.isfile(os.path.expanduser(sshconfig_path))   


def load_settings(envname=None):
    """
    Load settings into the fabric environnement and the tissu
    settings from a python file
    """
    set_current_tissu(None)

    if set_settings_module(envname) is False:
        msg = "Unable to find  %s settings" % envname
        raise ValueError(msg)

    from tissu.conf import settings as tissu_settings
    env.use_ssh_config = False
    if getattr(tissu_settings, C.FABRIC_USE_SSH_CONFIG, None):
        if env.ssh_config_path and sshconfig_exists(env.ssh_config_path):
            env.use_ssh_config = True

    roledefs = getattr(tissu_settings, C.ROLES, {})

    all_hosts = []
    setattr(env, C.HOSTDEFS, {})

    for role, hosts in roledefs.items():
        role_hosts = [hoststring_from_hostdef(host) for host in hosts]
        all_hosts += role_hosts
        env_attr_key_update(C.ROLEDEFS, role, role_hosts)

        passwords = {}
        for host in hosts:
            password = host.get(C.PASSWORD)
            if password is not None:
                key = hoststring_from_hostdef(host)
                passwords[key] = password

        env_attr_update(C.PASSWORDS, passwords)

        hostdefs = dict((hoststring_from_hostdef(host), host) for host in hosts)
        env_attr_update(C.HOSTDEFS, hostdefs)

        keys = [host.get(C.HOSTKEY) for host in hosts]
        for key in keys:
            if key is not None:
                if env.key_filename is None:
                    env.key_filename = [key, ]
                elif key not in env.key_filename:
                    env.key_filename.append(key)

    if len(getattr(env, C.ROLEDEFS)) == 0:
        msg = "Unable to load roles is '%s' defined in your settings file ?"
        raise KeyError(msg % C.ROLES)
    else:
        env_attr_key_update(C.ROLEDEFS, C.ALL_ROLE, list(set(all_hosts)))
        set_parallel_execution()
        setattr(env, C.MY_SETTINGS, tissu_settings)
        set_current_tissu(envname)
        return True

# EOF - vim: ts=4 sw=4 noet