#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Project   : Tissu - Functions to handle settings with Fabric
# -----------------------------------------------------------------------------
# License   : BSD License
# -----------------------------------------------------------------------------
# Authors   : Thierry Stiegler <thierry.stiegler@gmail.com>
# -----------------------------------------------------------------------------

from tissu.api import *
print(load_settings("caca"))


from tissu.conf import settings

public_props = (name for name in dir(settings) if not name.startswith('_'))
for k in public_props:
    print("%s : %s" % (k,getattr(settings, k) ) )

