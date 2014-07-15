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
    Handle your settings with Fabric

    Usage in your python code:

    >>> from tissu.api import *
    >>> load_settings(mysettings)

    >>> from tissu.conf import settings
    >>> my_setting = gettattr(settings, "my_settings")

    Usage in your fabfile:

    >>> from tissu.tasks import *

    $ fab e:mysettings

"""

import tissu.api
import tissu.tasks
import tissu.conf
from tissu.constants import VERSION


__all__ = [
    'api',
    'tasks',
    'constants',
    'conf',
    'VERSION'
]

__version__ = VERSION

# EOF - vim: ts=4 sw=4 noet