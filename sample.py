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
Sample module
"""

from tissu.api import load_settings
print load_settings("test")

from tissu.conf import settings

properties = [name for name in dir(settings) if not name.startswith('_')]
for k in properties:
    print "%s : %s" % (k, getattr(settings, k))
