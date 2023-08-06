.. vim: set fileencoding=utf-8 :

.. Copyright (c) 2016 Idiap Research Institute, http://www.idiap.ch/          ..
.. Contact: beat.support@idiap.ch                                             ..
..                                                                            ..
.. This file is part of the beat.cmdline module of the BEAT platform.         ..
..                                                                            ..
.. Commercial License Usage                                                   ..
.. Licensees holding valid commercial BEAT licenses may use this file in      ..
.. accordance with the terms contained in a written agreement between you     ..
.. and Idiap. For further information contact tto@idiap.ch                    ..
..                                                                            ..
.. Alternatively, this file may be used under the terms of the GNU Affero     ..
.. Public License version 3 as published by the Free Software and appearing   ..
.. in the file LICENSE.AGPL included in the packaging of this file.           ..
.. The BEAT platform is distributed in the hope that it will be useful, but   ..
.. WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY ..
.. or FITNESS FOR A PARTICULAR PURPOSE.                                       ..
..                                                                            ..
.. You should have received a copy of the GNU Affero Public License along     ..
.. with the BEAT platform. If not, see http://www.gnu.org/licenses/.          ..


.. _beat-cmdline-configuration:

Configuration
-------------

The ``beat`` command-line utility can operate independently of any initial
configuration. By runig for example the following command:

.. code-block:: sh

   $ beat dataformats list --remote

By default, ``beat`` is pre-configured to access the `main BEAT
website`_ anonymously, but it can be configured to use secret keys for any of
its users and/or access an alternative website installed somewhere else. This
allows users to push modified objects into the platform, completing the
development loop:

1. Pull objects of interest locally.
2. Develop new objects or modify existing ones.
3. Test locally, on an environment similar to the one available at the remote platform. (If the user wants to run the experiment locally without pushing it back to the platform they can use their own environment)
4. Push back modifications and then scale-up experiment running to explore more databases and more parameter combinations.

In order to properly configure a working prefix and memorize access options on
that directory, do the following from your shell:

.. code-block:: sh

   $ beat config set user myname token thistoken
   ...

You can verify your username and token have been memorized on that working
directory with:

.. command-output:: beat config show


By default, the command-line program considers the ``prefix`` directory on your
current working directory as your prefix. You can override this setting using the
``--prefix`` flag:

.. code-block:: sh

   $ beat --prefix=/Users/myname/work/beat config show
   ...


Note that it is also possible to set a different code editor

.. code-block:: sh

   $ beat config set editor vim


So we can imagine using the ``edit`` command to edit locally any object.

For example editing an algorithm named ``user/integers_echo/1`` can be done
using the following command:

.. code-block:: sh

   $ beat algorithm edit user/integers_echo/1

You can also use the ``path`` command on all your objects to identify all
the files and local paths for any given object.

For example we can get the files path associated with the algorithm
named ``user/integers_echo/1`` using the following command:

.. code-block:: sh

   $ beat algorithm path user/integers_echo/1


Local Overrides
===============

If you use the ``config set`` flag ``--local``, then the configuration values
are not set on the default configuration file (``~/.beatrc``), but instead in
the **current** working directory (``./.beatrc``). Configuration values found
the local directory take **precedence** over values configured on the global
file. Values from the command-line (such as those passed with ``--prefix`` as
explained above) take precedence over both settings.

You can set a variable on the local directory to override the global settings
like this:

.. code-block:: sh

   # set a different prefix when operating from the current directory
   $ beat config set --local prefix `pwd`/other_prefix
   $ beat config show
   ...


Database Root Directories
=========================

When running an experiment in the BEAT ecosystem using the local
executor (the default executor, also behind the ``--local`` flag), ``beat`` 
will look into your configuration for any options set by the user that follow
the format ``database/<db name>/<db version>``. ``beat`` expects that this
option points to a string representing the path to the root folder of the
actual database files for the given database.

For example, the AT&T "Database of Faces" is available on the BEAT platform
as the "atnt" database. The third version of the "atnt" database would be
referenced as "atnt/3". The object "atnt/3" has a root folder defined on
the BEAT platform already, and changing this locally would mean creating a
new version of the database.
Instead, you may override that path by setting the configuration option
``database/atnt/3`` to your local path to the database files.
Assuming your username is "user" and you extracted the database files to
``~/Downloads/atnt_db``, you can set ``database/atnt/3`` to
``/home/user/Downloads/atnt_db``, and BEAT will find the database files.

You may explore different configuration options with the ``--help`` flag of
``beat config``:

.. command-output:: beat config --help

.. include:: links.rst
