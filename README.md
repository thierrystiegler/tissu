About
=====

Functions to handle settings with Fabric


Usage
=====

Usage in your python code:

::
	>>> from tissu.api import *
	>>> load_settings(mysettings)

	>>> from tissu.conf import settings
	>>> my_setting = gettattr(settings, "my_settings")


Usage in your fabfile:
::
	>>> from tissu.tasks import *

	$ fab e:mysettings


INSTALLATION
============

Tissu is on PyPI so you can either use ``easy_install -U tissu``
or ``pip install tissu`` to install it. Otherwise, you can download
the source from `GitHub <http://github.com/thierrystiegler/tissu>`_ and
run ``python setup.py install``.



LICENCE
=======

BSD