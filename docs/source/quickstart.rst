.. quickstart

Quickstart
===========


First, you need to import tissu tasks.

So in your fabfile.py add this few lines

::
	from tissu.tasks import *


:: 

	$ fab -l
	Available commands:

	    e               Environnement loader
	    tissu_init      Init the settings scaffolding
	    tissu_print     Print FABRIC env dict and TISSU settings public properties



The you have 3 new tasks, *e* and *tissu_init*.

Now you have to generate the default settings scaffolding. That's the purpose of *tissu_init*.
By default, Tissu need a python module "settings.default".

Now, launch the taks *tissu_ini*




Tissu need a python module, by default *settings.default*.
(14:42:07) Thierry Stiegler: http://tissu.readthedocs.org/en/latest/
(14:42:23) _Fabien Schwob: Yeah ! plus qu'a remplir
(14:42:27) Thierry Stiegler: ouaip
(14:42:44) Thierry Stiegler: je sais jamais quoi mettre dedans...
(14:43:00) _Fabien Schwob: mais en gros, comment l'installer
(14:43:09) _Fabien Schwob: comment créer la configuration, où
(14:43:14) Thierry Stiegler: pip install tissu ?
(14:43:15) Thierry Stiegler: ;)
(14:43:21) _Fabien Schwob: oui mais meme ça
(14:43:26) Thierry Stiegler: ok
(14:43:35) Thierry Stiegler: je vais faire un quickstart
(14:43:53) Thierry Stiegler: de tout manière c'est pas très open comme module
(14:43:59) Thierry Stiegler: pas de notion de plugin de loaders
(14:44:04) Thierry Stiegler: et ce genre de connerie
(14:44:18) Thierry Stiegler: comment loader des settings via le code
(14:44:21) Thierry Stiegler: et via la commande fab ?
(14:44:26) _Fabien Schwob: yes
(14:44:36) Thierry Stiegler: et comment intégrer les commandes tissu dans ton fabfile
(14:44:37) Thierry Stiegler: ok
